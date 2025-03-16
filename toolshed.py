import streamlit as st

# Set page configuration (must be first)
st.set_page_config(layout="wide")

# Define tool lists
plan_tools = ["MoSCoW", "Five Whys", "VSM", "Affinity Diagram", "Fishbone Diagram"]
do_tools = ["Gemba", "Pilot Test", "5S", "Standard Work", "Process Mapping"]
check_tools = ["Control Charts", "Audit", "Survey", "Feedback Loop", "Benchmarking"]
act_tools = ["PDCA Cycle", "Lessons Learned", "Training", "Process Change", "Kaizen Event"]

# Function to ensure unique tool selection
def unique_selectbox(label, options, key, selected_options):
    available_options = [option for option in options if option not in selected_options]
    
    # Ensure there are still available tools
    if not available_options:
        st.warning("All tools in this section have been selected. Please choose different tools.")
        return None

    # Ensure unique keys by prefixing them with the section name
    selection = st.selectbox(label, available_options, key=f"{key}_unique")
    selected_options.append(selection)
    return selection

# Sidebar with color-coded headers
with st.sidebar:
    with st.expander("📌 Plan", expanded=False):
        st.markdown("<h3 style='color: #FFFF66;'>🟡 Plan</h3>", unsafe_allow_html=True)
        plan_selected = []
        plan_tool_1 = unique_selectbox("Select a Plan tool", plan_tools, "plan1", plan_selected)
        plan_tool_2 = unique_selectbox("Select another Plan tool", plan_tools, "plan2", plan_selected)
        plan_tool_3 = unique_selectbox("Select one more Plan tool", plan_tools, "plan3", plan_selected)

    with st.expander("🛠️ Do", expanded=False):
        st.markdown("<h3 style='color: #66FF66;'>🟢 Do</h3>", unsafe_allow_html=True)
        do_selected = []
        do_tool_1 = unique_selectbox("Select a Do tool", do_tools, "do1", do_selected)
        do_tool_2 = unique_selectbox("Select another Do tool", do_tools, "do2", do_selected)
        do_tool_3 = unique_selectbox("Select one more Do tool", do_tools, "do3", do_selected)

    with st.expander("✅ Check", expanded=False):
        st.markdown("<h3 style='color: #66CCFF;'>🔵 Check</h3>", unsafe_allow_html=True)
        check_selected = []
        check_tool_1 = unique_selectbox("Select a Check tool", check_tools, "check1", check_selected)
        check_tool_2 = unique_selectbox("Select another Check tool", check_tools, "check2", check_selected)
        check_tool_3 = unique_selectbox("Select one more Check tool", check_tools, "check3", check_selected)

    with st.expander("🚀 Act", expanded=False):
        st.markdown("<h3 style='color: #FF6666;'>🔴 Act</h3>", unsafe_allow_html=True)
        act_selected = []
        act_tool_1 = unique_selectbox("Select an Act tool", act_tools, "act1", act_selected)
        act_tool_2 = unique_selectbox("Select another Act tool", act_tools, "act2", act_selected)
        act_tool_3 = unique_selectbox("Select one more Act tool", act_tools, "act3", act_selected)

# Main content with tabs
st.title("CDH Continuous Improvement Toolshed")
st.markdown("## Welcome to the CI Tool Shed")
st.write("This section provides tools and techniques for continuous improvement.")

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["Tool Shed", "Tool Dictionary", "Video Library"])

with tab1:
    st.header("🛠️ Tool Shed")
    st.write("This section provides a collection of tools for Continuous Improvement (CI).")

with tab2:
    st.header("📖 Tool Dictionary")
    st.write("This section contains definitions and explanations of various tools.")

with tab3:
    st.header("🎥 Video Library")
    st.write("This section provides video resources for learning more about CI tools.")
