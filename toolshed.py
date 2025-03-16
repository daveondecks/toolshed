import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Set wide layout
st.set_page_config(layout="wide")

# Define tools under each category
plan_tools = ["MoSCoW", "Five Ys", "VSM", "Flow Chart", "Six S’s", "Process Map", "DMAIC", "RACI", "Route Cause", "VOC"]
do_tools = ["Gemba", "Kaizen", "SPC", "Kanban", "Pareto Chart", "Regression", "Poka-yoke", "SIPOC", "FMEA", "Asana"]
check_tools = ["Control Charts", "Check sheet", "Dashboard", "X-Matrix", "Heat Map", "Estimation", "DPMO", "Benchmarking", "Discovery", "Testing"]
act_tools = ["Deployment", "Quality", "Time", "Comms", "TQM", "Standard Work", "Lessons", "Risk Matrix", "Stakeholders", "Change Mgt"]

st.title("CDH Continuous Improvement Toolshed")

# Function to ensure unique tool selection
def unique_selectbox(label, options, key, selected_options):
    available_options = [option for option in options if option not in selected_options]
    if not available_options:
        st.warning("All tools in this section have been selected. Please choose different tools.")
        return None
    selection = st.sidebar.selectbox(label, available_options, key=key)
    selected_options.append(selection)
    return selection

# Sidebar with color-coded headers
with st.sidebar:
    with st.expander("📌 Plan", expanded=False):
        st.markdown("<h3 style='color: #FFFF66;'>🟡 Plan</h3>", unsafe_allow_html=True)
        # Ensure unique tool selection
        plan_selected = []
        plan_tool_1 = unique_selectbox("Select a Plan tool", plan_tools, "plan1", plan_selected)
        plan_tool_2 = unique_selectbox("Select another Plan tool", plan_tools, "plan2", plan_selected)
        plan_tool_3 = unique_selectbox("Select one more Plan tool", plan_tools, "plan3", plan_selected)
    
    with st.expander("🛠️ Do", expanded=False):
        st.markdown("<h3 style='color: #99CCFF;'>🔵 Do</h3>", unsafe_allow_html=True)
        do_selected = []
        do_selection = [
            unique_selectbox("Select a Do tool", do_tools, "do1", do_selected),
            unique_selectbox("Select another Do tool", do_tools, "do2", do_selected),
            unique_selectbox("Select one more Do tool", do_tools, "do3", do_selected)
        ]

    with st.expander("✅ Check", expanded=False):
        st.markdown("<h3 style='color: #99FF99;'>🟢 Check</h3>", unsafe_allow_html=True)
        check_selected = []
        check_selection = [
            unique_selectbox("Select a Check tool", check_tools, "check1", check_selected),
            unique_selectbox("Select another Check tool", check_tools, "check2", check_selected),
            unique_selectbox("Select one more Check tool", check_tools, "check3", check_selected)
        ]

    with st.expander("🚀 Act", expanded=False):
        st.markdown("<h3 style='color: #FFCC99;'>🟠 Act</h3>", unsafe_allow_html=True)
        act_selected = []
        act_selection = [
            unique_selectbox("Select an Act tool", act_tools, "act1", act_selected),
            unique_selectbox("Select another Act tool", act_tools, "act2", act_selected),
            unique_selectbox("Select one more Act tool", act_tools, "act3", act_selected)
        ]

# PDCA step descriptions
descriptions = {
    "Plan": "**Identify the issue:** Define the problem, gather relevant data. Formulate a hypothesis. What exactly are you trying to achieve by when? What resources do you need?",
    "Do": "**Quickly try out a solution:** Implement your plan, but start small. This stage is a controlled experiment, not full-scale deployment. Effective communication at this stage is key.",
    "Check": "**See if it works:** Step back and examine what happened. Did you get the desired result? Why or why not? Compare your actual outcomes against your predictions. Look for insights, opportunities, costs, lessons, or unexpected consequences.",
    "Act": "**Launch or adjust:** If your solution proved effective, how can you implement it more widely? If it fell short, what adjustments are needed? Perhaps you need to return to the planning stage with new insights."
}

# Function to generate toolboxes with a curved top to look like a toolbox
def draw_tools_box(title, tools, color, description_key):
    with st.expander(f"ℹ️ {title} Info"):
        st.markdown(descriptions[description_key])
    
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Lower the curved toolbox handle even closer to the top of the rectangle
    arc = patches.Arc((0.5, 0.79), 0.6, 0.3, angle=0, theta1=0, theta2=180, color='black', lw=6)
    ax.add_patch(arc)
    ax.text(0.5, 0.81, "Tools", ha='center', va='center', fontsize=12, color='black', fontweight='bold')
    
    # Draw tool slots
    for i, tool in enumerate(tools):
        if tool:
            ax.add_patch(patches.Rectangle((0.1, 0.55 - i * 0.15), 0.8, 0.12, color=color, ec='black', lw=2))
            ax.text(0.5, 0.61 - i * 0.15, tool, ha='center', va='center', fontsize=10, color='black')
    
    ax.set_title(title, fontsize=14, fontweight='bold')
    return fig

# Adjusted layout for proper PDCA quadrant alignment
col1, col3 = st.columns([1, 1])

with col1:
    st.pyplot(draw_tools_box("Plan Tools", plan_selection, "#FFFF66", "Plan"))  # Yellow
    st.pyplot(draw_tools_box("Act Tools", act_selection, "#FFCC99", "Act"))  # Orange

with col3:
    st.pyplot(draw_tools_box("Do Tools", do_selection, "#99CCFF", "Do"))  # Blue
    st.pyplot(draw_tools_box("Check Tools", check_selection, "#99FF99", "Check"))  # Green

st.success("Select the best tools for your Continuous Improvement journey!")
