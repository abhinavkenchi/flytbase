import sys
from pathlib import Path
import time
import math

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

    st.session_state.history[drone_id] = \
        st.session_state.history[drone_id][-6:]

# =====================================================
# CONFLICT DETECTION
# =====================================================
alerts = []
risk_ids = set()
conflict_objects = []

for i in range(len(df)):
    for j in range(i + 1, len(df)):

        r1 = df.iloc[i]
        r2 = df.iloc[j]

        x1 = float(r1["x"])
        y1 = float(r1["y"])

        x2 = float(r2["x"])
        y2 = float(r2["y"])

        id1 = str(r1["id"])
        id2 = str(r2["id"])

        dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

        if dist < 1.5:

            if dist < 0.6:
                severity = "high"
            elif dist < 1.0:
                severity = "medium"
            else:
                severity = "low"

            alerts.append(
                f"⚠ {id1} near {id2} | Distance {dist:.2f}"
            )

            risk_ids.add(id1)
            risk_ids.add(id2)

            conflict_objects.append({
                "severity": severity,
                "conflict_time": st.session_state.tick,
                "drone_a": id1,
                "drone_b": id2,
                "distance": dist
            })

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

    # Drone markers
    for _, row in df.iterrows():

        drone_id = str(row["id"])
        x = float(row["x"])
        y = float(row["y"])
        risk = str(row["risk"])

        if risk == "Conflict":
            color = "red"
            size = 22
        else:
            color = "green"
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