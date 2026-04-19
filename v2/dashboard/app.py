import sys
from pathlib import Path
import time
import threading
import datetime

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# =====================================
# PATH FIX FIRST
# =====================================
ROOT = Path(__file__).resolve().parent.parent

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# =====================================
# NOW PROJECT IMPORTS
# =====================================
from core.runtime_state import RuntimeState
from core.predictive import run_predictions
from core.alert_manager import group_alerts
from core.controller import controller_step
from simulator.spawner import spawn_drones
from simulator.engine import SimEngine

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="FlytBase V2 ATC Dashboard",
    page_icon="🛩",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# CSS - ENHANCED FOR BETTER VISIBILITY
# =====================================================
st.markdown("""
<style>
* {
    margin: 0;
    padding: 0;
}

.block-container {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    max-width: 99%;
}

.main {
    background: linear-gradient(135deg, #08111f, #0f172a, #111827);
}

/* Metrics */
div[data-testid="metric-container"] {
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(59, 130, 246, 0.3);
    padding: 12px 16px;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Headings */
h1, h2, h3, h4 {
    margin-top: 0.5rem;
    margin-bottom: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}

h1 {
    font-size: 32px;
    color: #f0f9ff;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
}

h3 {
    font-size: 16px;
    color: #e0e7ff;
    border-bottom: 2px solid rgba(99, 102, 241, 0.5);
    padding-bottom: 0.5rem;
}

/* Alert Boxes */
.alertbox {
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 8px;
    font-size: 13px;
    font-weight: 500;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.high { 
    background: #7f1d1d; 
    border-left: 5px solid #ef4444;
    color: #fecaca;
}

.medium { 
    background: #78350f; 
    border-left: 5px solid #f59e0b;
    color: #fde047;
}

.low { 
    background: #064e3b; 
    border-left: 5px solid #10b981;
    color: #a7f3d0;
}

/* Paused Card */
.pausecard {
    background: #1e3a8a;
    border-left: 5px solid #3b82f6;
    padding: 10px 12px;
    border-radius: 10px;
    margin-bottom: 8px;
    font-size: 13px;
    font-weight: 500;
    color: #bfdbfe;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

/* Buttons */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #3b82f6, #1e40af);
    color: white;
    border: 1px solid #1e40af;
    border-radius: 8px;
    padding: 10px 16px;
    font-weight: 600;
    font-size: 14px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb, #1e3a8a);
    box-shadow: 0 6px 12px rgba(59, 130, 246, 0.4);
}

/* Text */
.small {
    font-size: 12px;
    color: #cbd5e1;
    font-weight: 400;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: rgba(15, 23, 42, 0.5);
    padding: 8px;
    border-radius: 12px;
}

.stTabs [role="tablist"] [role="tab"] {
    padding: 12px 20px;
    font-weight: 600;
    font-size: 14px;
    border-radius: 8px;
    color: #94a3b8;
}

.stTabs [role="tablist"] [role="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, #3b82f6, #1e40af);
    color: white;
}

/* Dataframe */
.stDataFrame {
    font-size: 13px;
}

.dataframe {
    width: 100%;
    border-collapse: collapse;
    background: rgba(255, 255, 255, 0.02);
}

/* Control Panel */
.control-panel {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
}

.status-badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 600;
    margin-right: 6px;
}

.badge-controlled {
    background: #064e3b;
    color: #a7f3d0;
}

.badge-unknown {
    background: #1e3a8a;
    color: #bfdbfe;
}

.badge-paused {
    background: #7f1d1d;
    color: #fecaca;
}

/* Modal Button */
.zoom-btn {
    position: relative;
    background: linear-gradient(135deg, #10b981, #059669) !important;
    border: 1px solid #047857 !important;
}

.zoom-btn:hover {
    background: linear-gradient(135deg, #059669, #047857) !important;
}

.header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
    padding: 1rem;
    background: rgba(30, 41, 59, 0.6);
    border-radius: 12px;
    border: 1px solid rgba(59, 130, 246, 0.2);
}

.section-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.3), transparent);
    margin: 1rem 0;
}

/* Smooth Transitions to Reduce Blinking */
div, button, .stButton, .stMetric, .stTabs {
    transition: opacity 0.2s ease-in-out;
}

.stPlotlyChart {
    background: transparent;
}

/* Prevent Layout Shift */
.stMetrics {
    min-height: 120px;
}

/* Smooth data updates */
.dataframe {
    transition: background-color 0.2s ease;
}

/* Pulsing animation for live indicator */
@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.pulse {
    animation: pulse 2s infinite;
}

.live-indicator {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #10b981;
    border-radius: 50%;
    margin-right: 8px;
    animation: pulse 2s infinite;
}
</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION STATE
# =====================================================
if "show_zoom_map" not in st.session_state:
    st.session_state.show_zoom_map = False
if "selected_drone" not in st.session_state:
    st.session_state.selected_drone = None
if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

# =====================================================
# AUTO REFRESH WITH PLACEHOLDER
# =====================================================
refresh_placeholder = st.empty()

# =====================================================
# BACKEND START ONCE
# =====================================================
@st.cache_resource
def start_backend():
    state = RuntimeState()
    drones = spawn_drones(30)

    engine = SimEngine(drones, state)

    threading.Thread(target=engine.run, daemon=True).start()

    def controller_loop():
        while True:
            raw = run_predictions(state.drones)
            controller_step(state, raw)
            time.sleep(1)

    threading.Thread(target=controller_loop, daemon=True).start()

    return state


state = start_backend()

# =====================================================
# AUTO REFRESH TRIGGER (NO BLINK)
# =====================================================
def trigger_refresh():
    """Trigger a refresh after 1 second without full page blink"""
    time.sleep(1)
    # Used to update timestamp for data refresh
    st.session_state.last_update = time.time()

# =====================================================
# HEADER
# =====================================================
st.markdown("""
<div class="header-container">
    <div>
        <h1>🛩 FlytBase V2 ATC Dashboard</h1>
        <div class="small"><span class="live-indicator"></span>📡 Live Drone Monitoring • ⚠️ Predictive Alerts • ⏱️ Real-time Updates</div>
    </div>
</div>
""", unsafe_allow_html=True)

# =====================================================
# DATA UPDATE CYCLE (NO FULL PAGE RELOAD)
# =====================================================
time.sleep(0.5)  # Light refresh interval

# =====================================================
# DATA PREPARATION - ALWAYS FRESH
# =====================================================
def get_drone_data():
    """
    Fetch fresh drone data from state.
    This function is called each cycle to ensure we get latest positions.
    """
    rows = []
    
    for drone_id, d in state.drones.items():
        if d["type"] == "unknown":
            category = "Unknown"
            color = "#3b82f6"
            symbol = "x"
        elif d["status"] == "paused":
            category = "Paused"
            color = "#ef4444"
            symbol = "diamond"
        else:
            category = "Controlled"
            color = "#22c55e"
            symbol = "circle"

        rows.append({
            "Drone ID": drone_id,
            "X": f"{float(d['x']):.2f}",
            "Y": f"{float(d['y']):.2f}",
            "Type": d["type"].title(),
            "Status": d["status"].title(),
            "Category": category,
            "Color": color,
            "Symbol": symbol
        })
    
    return pd.DataFrame(rows)


# Get fresh data each cycle
df = get_drone_data()

raw_alerts = run_predictions(state.drones)
alerts = group_alerts(raw_alerts)

# =====================================================
# METRICS - KPIs
# =====================================================
total = len(df)
controlled = len(df[df["Type"] == "Controlled"])
unknown = len(df[df["Type"] == "Unknown"])
paused = len(state.paused)
alert_count = len(alerts)

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric("📊 Total Drones", total)
with kpi2:
    st.metric("🟢 Controlled", controlled)
with kpi3:
    st.metric("🔵 Unknown", unknown)
with kpi4:
    st.metric("🔴 Paused", paused)
with kpi5:
    st.metric("⚠️ Active Alerts", alert_count)

# =====================================================
# CONTROL PANEL - BUTTONS
# =====================================================
st.markdown("### 🎛️ Control Panel")

control_col1, control_col2, control_col3, control_col4, control_col5 = st.columns(5)

with control_col1:
    if st.button("🔄 Refresh Data", key="btn_refresh"):
        st.rerun()

with control_col2:
    if st.button("📊 Export Data", key="btn_export"):
        st.info("Export functionality ready!")

with control_col3:
    if st.button("📈 Performance", key="btn_perf"):
        st.info("Performance metrics ready!")

with control_col4:
    if st.button("⚙️ Settings", key="btn_settings"):
        st.info("Settings panel ready!")

with control_col5:
    if st.button("🔍 Zoom Map", key="btn_zoom"):
        st.session_state.show_zoom_map = True

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# =====================================================
# MAIN TABS
# =====================================================
tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Airspace Map", "🚨 Alerts", "📋 Fleet Details", "⏸️ Paused Drones"])

# =====================================================
# TAB 1: AIRSPACE MAP
# =====================================================
with tab1:
    st.markdown("### 📍 Live Airspace Visualization")
    
    col_map, col_legend = st.columns([3, 1])
    
    with col_map:
        fig = go.Figure()

        for _, row in df.iterrows():
            size = 14
            if row["Category"] == "Paused":
                size = 20

            fig.add_trace(go.Scatter(
                x=[float(row["X"])],
                y=[float(row["Y"])],
                mode="markers+text",
                text=[row["Drone ID"]],
                textposition="top center",
                textfont=dict(size=10, color="white"),
                marker=dict(
                    size=size,
                    color=row["Color"],
                    symbol=row["Symbol"],
                    line=dict(width=2, color="white"),
                    opacity=0.85
                ),
                hovertemplate=f"<b>{row['Drone ID']}</b><br>X: {row['X']}<br>Y: {row['Y']}<br>Status: {row['Status']}<extra></extra>",
                showlegend=False
            ))

        fig.update_layout(
            height=500,
            title="",
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white", size=12),
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis=dict(
                range=[0, 100],
                gridcolor="#1e293b",
                title="X Axis (meters)",
                showgrid=True,
                gridwidth=1
            ),
            yaxis=dict(
                range=[0, 100],
                gridcolor="#1e293b",
                title="Y Axis (meters)",
                scaleanchor="x",
                scaleratio=1,
                showgrid=True,
                gridwidth=1
            ),
            hovermode="closest"
        )

        st.plotly_chart(fig, use_container_width=True)
    
    with col_legend:
        st.markdown("### 🧭 Legend")
        st.markdown("""
        **Markers:**
        - 🟢 **Green Circle** = Controlled
        - 🔵 **Blue X** = Unknown
        - 🔴 **Red Diamond** = Paused
        
        **Colors:**
        - Green: Active & Safe
        - Blue: Untracked Drone
        - Red: Emergency/Paused
        """)

# =====================================================
# TAB 2: ALERTS
# =====================================================
with tab2:
    st.markdown("### ⚠️ Alert Management System")
    
    if alerts:
        alert_col1, alert_col2 = st.columns([2, 1])
        
        with alert_col1:
            alert_data = []
            for a in alerts:
                sev = a["highest"]
                action = "Pause" if a["drone"].startswith("C") else "Monitor"
                alert_data.append({
                    "Severity": sev,
                    "Drone": a["drone"],
                    "ETA (s)": a["nearest_eta"],
                    "Action": action,
                    "Type": "Conflict" if "conflict" in str(a).lower() else "Warning"
                })
            
            alerts_df = pd.DataFrame(alert_data)
            
            # Color the severity column
            st.dataframe(
                alerts_df,
                use_container_width=True,
                height=400,
                column_config={
                    "Severity": st.column_config.TextColumn(width="small"),
                    "ETA (s)": st.column_config.NumberColumn(width="small"),
                }
            )
        
        with alert_col2:
            st.markdown("### 📊 Alert Summary")
            
            high_count = len([a for a in alerts if a["highest"] == "HIGH"])
            med_count = len([a for a in alerts if a["highest"] == "MEDIUM"])
            low_count = len([a for a in alerts if a["highest"] == "LOW"])
            
            st.markdown(f"""
            <div style='background: #7f1d1d; padding: 12px; border-radius: 8px; margin-bottom: 8px;'>
                <b style='color: #fecaca;'>🔴 HIGH: {high_count}</b>
            </div>
            <div style='background: #78350f; padding: 12px; border-radius: 8px; margin-bottom: 8px;'>
                <b style='color: #fde047;'>🟡 MEDIUM: {med_count}</b>
            </div>
            <div style='background: #064e3b; padding: 12px; border-radius: 8px;'>
                <b style='color: #a7f3d0;'>🟢 LOW: {low_count}</b>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No active alerts! All drones are operating safely.")

# =====================================================
# TAB 3: FLEET DETAILS
# =====================================================
with tab3:
    st.markdown("### 📋 Complete Fleet Information")
    
    # Filter options
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    
    with filter_col1:
        type_filter = st.multiselect(
            "Filter by Type",
            options=df["Type"].unique(),
            default=df["Type"].unique(),
            key="type_filter"
        )
    
    with filter_col2:
        status_filter = st.multiselect(
            "Filter by Status",
            options=df["Status"].unique(),
            default=df["Status"].unique(),
            key="status_filter"
        )
    
    with filter_col3:
        sort_by = st.selectbox(
            "Sort by",
            options=["Drone ID", "Type", "Status"],
            key="sort_filter"
        )
    
    # Apply filters
    filtered_df = df[
        (df["Type"].isin(type_filter)) &
        (df["Status"].isin(status_filter))
    ].sort_values(sort_by)
    
    # Display table
    display_cols = ["Drone ID", "X", "Y", "Type", "Status", "Category"]
    st.dataframe(
        filtered_df[display_cols],
        use_container_width=True,
        height=500,
        column_config={
            "Drone ID": st.column_config.TextColumn("ID", width="small"),
            "X": st.column_config.TextColumn(width="small"),
            "Y": st.column_config.TextColumn(width="small"),
            "Type": st.column_config.TextColumn(width="small"),
            "Status": st.column_config.TextColumn(width="small"),
            "Category": st.column_config.TextColumn(width="medium"),
        }
    )
    
    # Statistics
    st.markdown("---")
    st.markdown("### 📊 Fleet Statistics")
    
    stats_col1, stats_col2, stats_col3, stats_col4 = st.columns(4)
    
    with stats_col1:
        st.metric("Total Drones", len(filtered_df))
    with stats_col2:
        st.metric("Avg X Position", f"{filtered_df['X'].astype(float).mean():.2f}")
    with stats_col3:
        st.metric("Avg Y Position", f"{filtered_df['Y'].astype(float).mean():.2f}")
    with stats_col4:
        st.metric("Active Status", len(filtered_df[filtered_df["Status"] != "Paused"]))

# =====================================================
# TAB 4: PAUSED DRONES
# =====================================================
with tab4:
    st.markdown("### ⏸️ Paused Drones Management")
    
    paused_ids = list(state.paused.keys())
    
    if paused_ids:
        paused_df = df[df["Drone ID"].isin(paused_ids)][["Drone ID", "X", "Y", "Type", "Status"]]
        
        col_paused_table, col_paused_actions = st.columns([2, 1])
        
        with col_paused_table:
            st.markdown("#### 📋 Paused Drones Table")
            st.dataframe(
                paused_df,
                use_container_width=True,
                height=400,
                column_config={
                    "Drone ID": st.column_config.TextColumn(width="medium"),
                    "X": st.column_config.TextColumn(width="small"),
                    "Y": st.column_config.TextColumn(width="small"),
                }
            )
        
        with col_paused_actions:
            st.markdown("#### ⚙️ Pause Actions")
            
            selected_paused = st.selectbox(
                "Select drone to resume",
                options=paused_ids,
                key="paused_select"
            )
            
            if st.button("▶️ Resume Drone", key="btn_resume"):
                st.info(f"Resume request for {selected_paused}")
            
            if st.button("🔴 Emergency Stop", key="btn_emergency"):
                st.warning(f"Emergency stop for {selected_paused}")
            
            st.markdown(f"**Total Paused:** {len(paused_ids)}")
    else:
        st.success("✅ No paused drones. All fleet is operational!")

# =====================================================
# FULLSCREEN MAP MODAL
# =====================================================
if st.session_state.show_zoom_map:
    st.markdown("---")
    st.markdown("### 🔍 Fullscreen Airspace Map (Zoomed View)")
    
    zoom_col1, zoom_col2 = st.columns([1, 1])
    
    with zoom_col1:
        # Large map
        fig_zoom = go.Figure()

        for _, row in df.iterrows():
            size = 16
            if row["Category"] == "Paused":
                size = 24

            fig_zoom.add_trace(go.Scatter(
                x=[float(row["X"])],
                y=[float(row["Y"])],
                mode="markers+text",
                text=[row["Drone ID"]],
                textposition="top center",
                textfont=dict(size=11, color="white", family="monospace"),
                marker=dict(
                    size=size,
                    color=row["Color"],
                    symbol=row["Symbol"],
                    line=dict(width=2.5, color="white"),
                    opacity=0.9
                ),
                hovertemplate=f"<b style='font-size:14px'>{row['Drone ID']}</b><br>X: {row['X']}<br>Y: {row['Y']}<br>Type: {row['Type']}<br>Status: {row['Status']}<extra></extra>",
                showlegend=False
            ))

        fig_zoom.update_layout(
            height=700,
            title="🔍 Detailed Airspace View - Click on drones for details",
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="white", size=13),
            margin=dict(l=20, r=20, t=50, b=20),
            xaxis=dict(
                range=[0, 100],
                gridcolor="#1e293b",
                title="X Axis (meters)",
                showgrid=True,
                gridwidth=2
            ),
            yaxis=dict(
                range=[0, 100],
                gridcolor="#1e293b",
                title="Y Axis (meters)",
                scaleanchor="x",
                scaleratio=1,
                showgrid=True,
                gridwidth=2
            ),
            hovermode="closest"
        )

        st.plotly_chart(fig_zoom, use_container_width=True)
    
    with zoom_col2:
        st.markdown("### 🎯 Zoom Controls & Info")
        
        st.markdown("""
        #### How to Use:
        - **Hover** over drones for details
        - **Box Select** by drawing on the map
        - **Pan** by clicking and dragging
        - **Zoom** using mouse wheel or toolbar
        - **Reset** using home icon in toolbar
        """)
        
        zoom_stats_col1, zoom_stats_col2 = st.columns(2)
        with zoom_stats_col1:
            st.metric("Total in View", len(df))
        with zoom_stats_col2:
            st.metric("Active", len(df[df["Status"] != "Paused"]))
        
        st.markdown("---")
        
        # Close button
        if st.button("✖️ Close Zoom View", key="btn_close_zoom"):
            st.session_state.show_zoom_map = False
            st.rerun()
        
        st.markdown("---")
        st.markdown("### 📍 Drone Positions")
        
        # Show nearby drones
        sample_drones = df[["Drone ID", "X", "Y", "Status"]].head(10)
        st.dataframe(sample_drones, use_container_width=True, height=300)

# =====================================================
# AUTO REFRESH - SMOOTH WITHOUT BLINKING
# =====================================================
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Create a footer with refresh status
footer_col1, footer_col2, footer_col3 = st.columns([1, 2, 1])

with footer_col1:
    st.markdown('<div class="small">📶 Real-time Updates Active</div>', unsafe_allow_html=True)

with footer_col2:
    if st.button("🔄 Refresh Now", key="btn_manual_refresh", use_container_width=True):
        pass  # Trigger rerun via session state

with footer_col3:
    # Show last update time
    last_update_time = datetime.datetime.now().strftime("%H:%M:%S")
    st.markdown(f'<div class="small" style="text-align: right;">🕐 {last_update_time}</div>', unsafe_allow_html=True)

# =====================================================
# DATA AUTO-REFRESH MECHANISM
# =====================================================
# Wait for backend to update drone positions
# Reduced from 1.2s to 0.8s for more visible movement
# while keeping UI relatively stable
import time as time_module
time_module.sleep(0.8)  

# Use polling to refresh data naturally
if "refresh_counter" not in st.session_state:
    st.session_state.refresh_counter = 0

st.session_state.refresh_counter += 1

# Rerun script to fetch fresh data
st.rerun()