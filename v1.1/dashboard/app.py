import sys
from pathlib import Path
import time

import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# =====================================================
# PATH FIX FIRST
# =====================================================
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

from simulator.telemetry import generate_drones
from core.resolution import suggest_resolution
from core.dashboard_engine import detect_live_conflicts
from core.predictive import predict_future_conflicts

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="UAV Strategic Dashboard",
    page_icon="🛩",
    layout="wide"
)

st.markdown(
    """
    <h1 style='margin-bottom:0;'>🛩 UAV Strategic Deconfliction Dashboard</h1>
    <p style='color:gray;margin-top:0;'>
    Real-Time Airspace Monitoring • Conflict Prevention • Animation Playback • Auto Resolution
    </p>
    """,
    unsafe_allow_html=True
)

# =====================================================
# SESSION STATE
# =====================================================
if "tick" not in st.session_state:
    st.session_state.tick = 0

if "running" not in st.session_state:
    st.session_state.running = False

if "history" not in st.session_state:
    st.session_state.history = {}

if "incident_log" not in st.session_state:
    st.session_state.incident_log = []

if "speed" not in st.session_state:
    st.session_state.speed = 1

MAX_TICK = 200

# =====================================================
# CONTROL PANEL
# =====================================================
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    if st.button("▶ Start", use_container_width=True):
        st.session_state.running = True

with c2:
    if st.button("⏸ Pause", use_container_width=True):
        st.session_state.running = False

with c3:
    if st.button("⏭ Step +1", use_container_width=True):
        st.session_state.tick += 1

with c4:
    if st.button("⚠ Jump Alert", use_container_width=True):
        st.session_state.tick = 90

with c5:
    if st.button("🔄 Reset", use_container_width=True):
        st.session_state.tick = 0
        st.session_state.running = False
        st.session_state.history = {}
        st.session_state.incident_log = []

# =====================================================
# PLAYBACK CONTROLS
# =====================================================
s1, s2 = st.columns(2)

with s1:
    st.session_state.tick = st.slider(
        "Simulation Timeline",
        0,
        MAX_TICK,
        st.session_state.tick
    )

with s2:
    st.session_state.speed = st.selectbox(
        "Playback Speed",
        [1, 2, 3, 5],
        index=0
    )

# =====================================================
# AUTO PLAY CLOCK
# =====================================================
if st.session_state.running:
    st.session_state.tick += st.session_state.speed

    if st.session_state.tick > MAX_TICK:
        st.session_state.tick = 0
        st.session_state.history = {}

# =====================================================
# LOAD DRONE DATA
# =====================================================
drones = generate_drones(st.session_state.tick)

df = pd.DataFrame(drones).astype({
    "id": "string",
    "x": "float64",
    "y": "float64",
    "status": "string"
})

# =====================================================
# STORE TRAILS
# =====================================================
for _, row in df.iterrows():

    drone_id = str(row["id"])

    if drone_id not in st.session_state.history:
        st.session_state.history[drone_id] = []

    st.session_state.history[drone_id].append(
        (float(row["x"]), float(row["y"]))
    )

    st.session_state.history[drone_id] = st.session_state.history[drone_id][-6:]

# =====================================================
# LIVE CONFLICT DETECTION
# =====================================================
alerts, risk_ids, conflict_objects = detect_live_conflicts(
    df,
    st.session_state.tick
)

for item in conflict_objects:
    st.session_state.incident_log.append(item)

st.session_state.incident_log = st.session_state.incident_log[-50:]

# =====================================================
# RISK COLUMN
# =====================================================
df["risk"] = df["id"].apply(
    lambda d: "Conflict" if d in risk_ids else "Safe"
)

# =====================================================
# KPI PANEL
# =====================================================
k1, k2, k3, k4 = st.columns(4)

k1.metric("Total Drones", len(df))
k2.metric("Active Alerts", len(alerts))
k3.metric(
    "System",
    "RUNNING" if st.session_state.running else "PAUSED"
)
k4.metric("Simulation Time (s)", st.session_state.tick)

# =====================================================
# MAIN LAYOUT
# =====================================================
left, right = st.columns([2.3, 1])

# =====================================================
# LIVE MAP
# =====================================================
with left:

    fig = go.Figure()

    trail_colors = [
        "#00BFFF",
        "#FFA500",
        "#FF69B4",
        "#9370DB",
        "#00FA9A"
    ]

    ids = list(st.session_state.history.keys())

    # Trails
    for idx, drone_id in enumerate(ids):

        pts = st.session_state.history[drone_id]

        if len(pts) >= 2:

            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]

            fig.add_trace(
                go.Scatter(
                    x=xs,
                    y=ys,
                    mode="lines",
                    line=dict(
                        width=2,
                        color=trail_colors[idx % len(trail_colors)]
                    ),
                    opacity=0.28,
                    showlegend=False,
                    hoverinfo="skip"
                )
            )

    # Drone Markers
    for _, row in df.iterrows():

        drone_id = str(row["id"])
        x = float(row["x"])
        y = float(row["y"])
        risk = str(row["risk"])

        if risk == "Conflict":
            color = "#dc2626"
            size = 22
        else:
            color = "#16a34a"
            size = 18

        fig.add_trace(
            go.Scatter(
                x=[x],
                y=[y],
                mode="markers+text",
                text=[drone_id],
                textposition="top center",
                marker=dict(
                    size=size,
                    color=color,
                    line=dict(width=1)
                ),
                showlegend=False
            )
        )

    fig.update_layout(
        title="Animated Airspace Playback",
        height=580,
        margin=dict(l=10, r=10, t=45, b=10),
        xaxis=dict(
            title="X Coordinate",
            range=[0, 20],
            showgrid=True
        ),
        yaxis=dict(
            title="Y Coordinate",
            range=[0, 20],
            showgrid=True
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
        config={"displayModeBar": False}
    )

# =====================================================
# RIGHT PANEL
# =====================================================
with right:

    st.subheader("Drone Status")

    show_df = df[
        ["id", "x", "y", "status", "risk"]
    ].copy()

    show_df["x"] = show_df["x"].round(2)
    show_df["y"] = show_df["y"].round(2)

    st.dataframe(
        show_df,
        use_container_width=True,
        height=320
    )

    # -----------------------------------------------
    # Conflict Alerts
    # -----------------------------------------------
    st.subheader("Conflict Alerts")

    if alerts:
        for a in alerts:
            st.error(a)

        st.subheader("Recommended Actions")

        first_conflict = conflict_objects[0]
        actions = suggest_resolution(first_conflict)

        for act in actions:
            st.info(act)

    else:
        st.success(
            "Airspace Safe ✅\n\n"
            "All separation minima maintained."
        )

    # -----------------------------------------------
    # Incident History
    # -----------------------------------------------
    st.subheader("Incident History")

    if st.session_state.incident_log:

        hist_df = pd.DataFrame(st.session_state.incident_log)

        st.dataframe(
            hist_df,
            use_container_width=True,
            height=220
        )

        csv = hist_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Incident Report",
            data=csv,
            file_name="incident_report.csv",
            mime="text/csv",
            use_container_width=True
        )

    else:
        st.caption("No incidents recorded yet.")

    # -----------------------------------------------
    # Predictive Alerts
    # -----------------------------------------------
    st.subheader("Predictive Alerts")

    future = predict_future_conflicts(
        st.session_state.tick,
        5
    )

    if future:
        for item in future:
            st.warning(
                f"T+{item['tick'] - st.session_state.tick}s : "
                f"{item['details']}"
            )
    else:
        st.success(
            "No predicted conflicts in next 5 seconds."
        )

    # -----------------------------------------------
    # Playback Notes
    # -----------------------------------------------
    st.subheader("Playback Notes")

    st.info(
        "▶ Start = Auto Play\n\n"
        "⏸ Pause = Freeze Motion\n\n"
        "⏭ Step = Advance 1 Tick\n\n"
        "⚠ Jump Alert = Conflict Moment\n\n"
        "🔄 Reset = Restart Simulation"
    )

# =====================================================
# REFRESH LOOP
# =====================================================
time.sleep(1)
st.rerun()