import streamlit as st
import pandas as pd

# Set page configuration
st.set_page_config(layout="wide")

# Initialize session state for tab selection
if "selected_tab" not in st.session_state:
    st.session_state["selected_tab"] = "Tool Shed"  # Default tab

# Load CSV Data (with Uppercase 'Data' folder)
@st.cache_data
def load_data():
    return pd.read_csv("Data/Tools_description.csv")  # 🔹 Corrected Path

tool_data = load_data()

# --- PDCA TOOLS LIST ---
plan_tools = ["MoSCoW", "Five Ys", "VSM", "Flow Chart", "Six S’s", "Process Map", "DMAIC", "RACI", "Root Cause", "VOC"]
do_tools = ["Gemba", "Kaizen", "SPC", "Kanban", "Pareto Chart", "Regression", "Poka-yoke", "SIPOC", "FMEA", "Asana"]
check_tools = ["Control Charts", "Check sheet", "Dashboard", "X-Matrix", "Heat Map", "Estimation", "DPMO", "Benchmarking", "Discovery", "Testing"]
act_tools = ["Deployment", "Quality", "Time", "Comms", "TQM", "Standard Work", "Lessons", "Risk Matrix", "Stakeholders", "Change Mgt"]

# --- SIDEBAR (PDCA Expanders + Selection Boxes) ---
with st.sidebar:
    with st.expander("📌 Plan", expanded=False):
        st.markdown("<h3 style='color: #FFFF66;'>🟡 Plan</h3>", unsafe_allow_html=True)
        plan_selected = []
        plan_selection = [
            st.selectbox("Select a Plan tool", plan_tools, key="plan1"),
            st.selectbox("Select another Plan tool", plan_tools, key="plan2"),
            st.selectbox("Select one more Plan tool", plan_tools, key="plan3")
        ]

    with st.expander("🛠️ Do", expanded=False):
        st.markdown("<h3 style='color: #99CCFF;'>🔨 Do</h3>", unsafe_allow_html=True)
        do_selected = []
        do_selection = [
            st.selectbox("Select a Do tool", do_tools, key="do1"),
            st.selectbox("Select another Do tool", do_tools, key="do2"),
            st.selectbox("Select one more Do tool", do_tools, key="do3")
        ]

    with st.expander("✅ Check", expanded=False):
        st.markdown("<h3 style='color: #99FF99;'>✅ Check</h3>", unsafe_allow_html=True)
        check_selected = []
        check_selection = [
            st.selectbox("Select a Check tool", check_tools, key="check1"),
            st.selectbox("Select another Check tool", check_tools, key="check2"),
            st.selectbox("Select one more Check tool", check_tools, key="check3")
        ]

    with st.expander("🚀 Act", expanded=False):
        st.markdown("<h3 style='color: #FFCC99;'>🚀 Act</h3>", unsafe_allow_html=True)
        act_selected = []
        act_selection = [
            st.selectbox("Select an Act tool", act_tools, key="act1"),
            st.selectbox("Select another Act tool", act_tools, key="act2"),
            st.selectbox("Select one more Act tool", act_tools, key="act3")
        ]

# --- TOP NAVIGATION TABS ---
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🛠️ Tool Shed", key="tool_shed"):
        st.session_state["selected_tab"] = "Tool Shed"

with col2:
    if st.button("📚 Tool Dictionary", key="tool_library"):
        st.session_state["selected_tab"] = "Tool Dictionary"

with col3:
    if st.button("🎥 Video Library", key="video_library"):
        st.session_state["selected_tab"] = "Video Library"

# --- DISPLAY CONTENT BASED ON SELECTED TAB ---
if st.session_state["selected_tab"] == "Tool Shed":
    st.header("🛠️ Tool Shed")
    st.write("This section provides a collection of tools for Continuous Improvement (CI).")

    # PDCA step descriptions
    descriptions = {
        "Plan": "**Identify the issue:** Define the problem, gather relevant data, and formulate a hypothesis.",
        "Do": "**Quickly try out a solution:** Implement the plan on a small scale before full-scale deployment.",
        "Check": "**See if it works:** Evaluate results, compare against predictions, and gain insights.",
        "Act": "**Launch or adjust:** Implement successful changes broadly, or refine and retry if needed."
    }

    # Function to display toolboxes
    def draw_tools_box(title, tools, description_key):
        with st.expander(f"ℹ️ {title} Info"):
            st.markdown(descriptions[description_key])

        st.markdown(f"### {title} Tools")
        st.write(", ".join(tools))  # Display tools as a simple list

    # 2x2 Grid Layout
    col1, col2 = st.columns(2)

    with col1:
        draw_tools_box("Plan Tools", plan_selection, "Plan")
        draw_tools_box("Act Tools", act_selection, "Act")

    with col2:
        draw_tools_box("Do Tools", do_selection, "Do")
        draw_tools_box("Check Tools", check_selection, "Check")

    st.success("✅ Select the best tools for your Continuous Improvement journey!")

elif st.session_state["selected_tab"] == "Tool Dictionary":
    st.header("📚 Tool Dictionary")
    st.write("Search and explore CI tools with descriptions and links.")

    search_query = st.text_input("🔍 Search for a tool:")
    filtered_data = tool_data[tool_data['Tool Name'].str.contains(search_query, case=False, na=False)]

    # Convert 'Tool Name' into clickable links
    filtered_data['Tool Name'] = filtered_data.apply(
        lambda row: f"[{row['Tool Name']}]({row['More Info']})" if pd.notna(row['More Info']) else row['Tool Name'],
        axis=1
    )

    # Display Searchable Table
    st.dataframe(filtered_data[['Tool Name', 'PDCA Category', 'Description']])

elif st.session_state["selected_tab"] == "Video Library":
    st.header("🎥 Video Library")
    st.write("Watch training videos on CI tools and methodologies.")

    # Placeholder for video content
    st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # Replace with relevant videos

st.success("🚀 Toolshed fully updated with sidebar tools, searchable database & PDCA tools!")