import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Set wide layout
st.set_page_config(layout="wide")

# Define tools under each category
plan_tools = ["MoSCoW", "Five Ys", "VSM", "Flow Chart", "Six S’s", "Process Map", "DMAIC", "RACI", "Route Cause", "VOC"]
do_tools = ["Gemba", "Kaizen", "SPC", "Kanban", "Pareto Chart", "Regression", "Poka-yoke", "SIPOC", "FMEA", "Asana"]
check_tools = ["Control Charts", "Check sheet", "Dashboard", "X-Matrix", "Heat Map", "Estimation", "DPMO", "Benchmarking", "Discovery", "Testing"]
act_tools = ["Deployment", "Quality", "Time", "Comms", "TQM", "Standard Work", "Lessons", "Risk Matrix", "Stakeholders", "Change Mgt"]

st.title("CDH Continuous Improvement Toolshed")

# Sidebar with color-coded headers
st.sidebar.markdown("<h3 style='color: #FFFF66;'>🟡 Plan</h3>", unsafe_allow_html=True)
plan_selection = [
    st.sidebar.selectbox("Select a Plan tool", plan_tools, key="plan1"),
    st.sidebar.selectbox("Select another Plan tool", plan_tools, key="plan2"),
    st.sidebar.selectbox("Select one more Plan tool", plan_tools, key="plan3")
]

st.sidebar.markdown("<h3 style='color: #99CCFF;'>🔵 Do</h3>", unsafe_allow_html=True)
do_selection = [
    st.sidebar.selectbox("Select a Do tool", do_tools, key="do1"),
    st.sidebar.selectbox("Select another Do tool", do_tools, key="do2"),
    st.sidebar.selectbox("Select one more Do tool", do_tools, key="do3")
]

st.sidebar.markdown("<h3 style='color: #99FF99;'>🟢 Check</h3>", unsafe_allow_html=True)
check_selection = [
    st.sidebar.selectbox("Select a Check tool", check_tools, key="check1"),
    st.sidebar.selectbox("Select another Check tool", check_tools, key="check2"),
    st.sidebar.selectbox("Select one more Check tool", check_tools, key="check3")
]

st.sidebar.markdown("<h3 style='color: #FFCC99;'>🟠 Act</h3>", unsafe_allow_html=True)
act_selection = [
    st.sidebar.selectbox("Select an Act tool", act_tools, key="act1"),
    st.sidebar.selectbox("Select another Act tool", act_tools, key="act2"),
    st.sidebar.selectbox("Select one more Act tool", act_tools, key="act3")
]

# Function to generate toolboxes with a curved top to look like a toolbox

def draw_tools_box(title, tools, color):
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Draw the curved toolbox handle
    ax.add_patch(plt.Rectangle((0.1, 0.8), 0.8, 0.15, color='black', ec='black', lw=2))
    ax.text(0.5, 0.87, "Tools", ha='center', va='center', fontsize=12, color='white', fontweight='bold')
    
    # Draw tool slots
    for i, tool in enumerate(tools):
        ax.add_patch(plt.Rectangle((0.1, 0.55 - i * 0.15), 0.8, 0.12, color=color, ec='black', lw=2))
        ax.text(0.5, 0.61 - i * 0.15, tool, ha='center', va='center', fontsize=10, color='black')
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    return fig

# Layout for toolboxes and central PDCA cycle indicator
col1, col2, col3 = st.columns([1, 0.5, 1])

with col1:
    st.pyplot(draw_tools_box("Plan Tools", plan_selection, "#FFFF66"))  # Yellow
    st.pyplot(draw_tools_box("Act Tools", act_selection, "#FFCC99"))  # Orange

# Center section with PDCA cycle arrows
with col2:
    fig, ax = plt.subplots(figsize=(2, 2))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Draw circular arrows to indicate clockwise PDCA cycle
    arrow_params = dict(head_width=0.05, head_length=0.05, fc='black', ec='black')
    ax.arrow(0.5, 0.85, 0.0, -0.3, **arrow_params)  # PLAN → DO
    ax.arrow(0.85, 0.5, -0.3, 0.0, **arrow_params)  # DO → CHECK
    ax.arrow(0.5, 0.15, 0.0, 0.3, **arrow_params)  # CHECK → ACT
    ax.arrow(0.15, 0.5, 0.3, 0.0, **arrow_params)  # ACT → PLAN
    
    ax.text(0.5, 0.5, "🔄", ha='center', va='center', fontsize=30)  # Large cycle icon
    st.pyplot(fig)

with col3:
    st.pyplot(draw_tools_box("Do Tools", do_selection, "#99CCFF"))  # Blue
    st.pyplot(draw_tools_box("Check Tools", check_selection, "#99FF99"))  # Green

st.success("Select the best tools for your Continuous Improvement journey!")
