import streamlit as st
import matplotlib.pyplot as plt

# Set wide layout
st.set_page_config(layout="wide")

# Define tools under each category
plan_tools = ["MoSCoW", "Five Ys", "VSM", "Flow Chart", "Six S’s", "Process Map", "DMAIC", "RACI", "Route Cause", "VOC"]
do_tools = ["Gemba", "Kaizen", "SPC", "Kanban", "Pareto Chart", "Regression", "Poka-yoke", "SIPOC", "FMEA", "Asana"]
check_tools = ["Control Charts", "Check sheet", "Dashboard", "X-Matrix", "Heat Map", "Estimation", "DPMO", "Benchmarking", "Discovery", "Testing"]
act_tools = ["Deployment", "Quality", "Time", "Comms", "TQM", "Standard Work", "Lessons", "Risk Matrix", "Stakeholders", "Change Mgt"]

st.title("CDH Continuous Improvement Toolshed")

st.sidebar.header("Select Tools for Each Phase")

plan_selection = [
    st.sidebar.selectbox("Select a Plan tool", plan_tools, key="plan1"),
    st.sidebar.selectbox("Select another Plan tool", plan_tools, key="plan2"),
    st.sidebar.selectbox("Select one more Plan tool", plan_tools, key="plan3")
]

do_selection = [
    st.sidebar.selectbox("Select a Do tool", do_tools, key="do1"),
    st.sidebar.selectbox("Select another Do tool", do_tools, key="do2"),
    st.sidebar.selectbox("Select one more Do tool", do_tools, key="do3")
]

check_selection = [
    st.sidebar.selectbox("Select a Check tool", check_tools, key="check1"),
    st.sidebar.selectbox("Select another Check tool", check_tools, key="check2"),
    st.sidebar.selectbox("Select one more Check tool", check_tools, key="check3")
]

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

# Arrange toolboxes in the same layout as the reference image
col1, col2 = st.columns(2)

with col1:
    st.pyplot(draw_tools_box("Plan Tools", plan_selection, "#FFFF66"))  # Yellow
    st.pyplot(draw_tools_box("Act Tools", act_selection, "#FFCC99"))  # Orange

with col2:
    st.pyplot(draw_tools_box("Do Tools", do_selection, "#99CCFF"))  # Blue
    st.pyplot(draw_tools_box("Check Tools", check_selection, "#99FF99"))  # Green

st.success("Select the best tools for your Continuous Improvement journey!")
