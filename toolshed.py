import streamlit as st
import pandas as pd
import datetime

# Set page configuration
st.set_page_config(layout="wide")

# Initialize session state for tab selection
if "selected_tab" not in st.session_state:
    st.session_state["selected_tab"] = "Tool Shed"  # Default tab

# Load CSV Data
@st.cache_data
def load_data():
    return pd.read_csv("Data/Tools_description.csv")  # Ensure correct path

tool_data = load_data()

# --- PDCA TOOLS LIST ---
plan_tools = ["MoSCoW", "Five Ys", "VSM", "Flow Chart", "Six S’s", "Process Map", "DMAIC", "RACI", "Root Cause", "VOC"]
do_tools = ["Gemba", "Kaizen", "SPC", "Kanban", "Pareto Chart", "Regression", "Poka-yoke", "SIPOC", "FMEA", "Asana"]
check_tools = ["Control Charts", "Check sheet", "Dashboard", "X-Matrix", "Heat Map", "Estimation", "DPMO", "Benchmarking", "Discovery", "Testing"]
act_tools = ["Deployment", "Quality", "Time", "Comms", "TQM", "Standard Work", "Lessons", "Risk Matrix", "Stakeholders", "Change Mgt"]

# --- Function to ensure unique tool selection ---
def unique_selectbox(label, options, key, selected_options):
    available_options = [option for option in options if option not in selected_options]
    if not available_options:
        st.warning(f"All {label} tools have been selected. Please change your choices.")
        return None
    selection = st.selectbox(label, available_options, key=key)
    selected_options.append(selection)
    return selection

# --- SIDEBAR (PDCA Expanders + Unique Selection Boxes) ---
with st.sidebar:
    with st.expander("📌 Plan", expanded=False):
        st.markdown("<h3 style='color: #FFFF66;'>🟡 Plan</h3>", unsafe_allow_html=True)
        plan_selected = []
        plan_selection = [
            unique_selectbox("Select a Plan tool", plan_tools, "plan1", plan_selected),
            unique_selectbox("Select another Plan tool", plan_tools, "plan2", plan_selected),
            unique_selectbox("Select one more Plan tool", plan_tools, "plan3", plan_selected)
        ]

    with st.expander("🛠️ Do", expanded=False):
        st.markdown("<h3 style='color: #99CCFF;'>🔨 Do</h3>", unsafe_allow_html=True)
        do_selected = []
        do_selection = [
            unique_selectbox("Select a Do tool", do_tools, "do1", do_selected),
            unique_selectbox("Select another Do tool", do_tools, "do2", do_selected),
            unique_selectbox("Select one more Do tool", do_tools, "do3", do_selected)
        ]

    with st.expander("✅ Check", expanded=False):
        st.markdown("<h3 style='color: #99FF99;'>✅ Check</h3>", unsafe_allow_html=True)
        check_selected = []
        check_selection = [
            unique_selectbox("Select a Check tool", check_tools, "check1", check_selected),
            unique_selectbox("Select another Check tool", check_tools, "check2", check_selected),
            unique_selectbox("Select one more Check tool", check_tools, "check3", check_selected)
        ]

    with st.expander("🚀 Act", expanded=False):
        st.markdown("<h3 style='color: #FFCC99;'>🚀 Act</h3>", unsafe_allow_html=True)
        act_selected = []
        act_selection = [
            unique_selectbox("Select an Act tool", act_tools, "act1", act_selected),
            unique_selectbox("Select another Act tool", act_tools, "act2", act_selected),
            unique_selectbox("Select one more Act tool", act_tools, "act3", act_selected)
        ]

# --- TOP NAVIGATION TABS ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("🛠️ Tool Shed", key="tool_shed"):
        st.session_state["selected_tab"] = "Tool Shed"

with col2:
    if st.button("📚 Tool Dictionary", key="tool_library"):
        st.session_state["selected_tab"] = "Tool Dictionary"

with col3:
    if st.button("🎥 Video Library", key="video_library"):
        st.session_state["selected_tab"] = "Video Library"

with col4:
    if st.button("📄 Project Plan", key="project_plan"):
        st.session_state["selected_tab"] = "Project Plan"

# --- DISPLAY CONTENT BASED ON SELECTED TAB ---
if st.session_state["selected_tab"] == "Tool Shed":
    st.header("🛠️ Tool Shed")
    st.write("This section provides a collection of tools for Continuous Improvement (CI).")

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

elif st.session_state["selected_tab"] == "Project Plan":
    st.header("📄 Project Plan Preview")

    # User Inputs for Project Plan
    project_name = st.text_input("📌 Enter Project Name")
    project_owner = st.text_input("👤 Enter Project Owner")
    date_created = datetime.date.today().strftime("%Y-%m-%d")

    if st.button("Generate Preview"):
        # Create Dataframe for Selected Tools and Descriptions
        selected_tools = {
            "Plan": plan_selection,
            "Do": do_selection,
            "Check": check_selection,
            "Act": act_selection
        }

        project_plan_data = []
        for category, tools in selected_tools.items():
            for tool in tools:
                if tool:
                    desc = tool_data[tool_data['Tool Name'] == tool]['Description'].values
                    project_plan_data.append({"Category": category, "Tool": tool, "Description": desc[0] if len(desc) > 0 else "N/A"})

        df = pd.DataFrame(project_plan_data)

        # Display Project Plan Preview
        st.write(f"### 📌 Project Name: {project_name}")
        st.write(f"👤 **Project Owner:** {project_owner}")
        st.write(f"📅 **Date Created:** {date_created}")

        if not df.empty:
            st.dataframe(df)
        else:
            st.warning("⚠️ No tools selected yet!")

st.success("🚀 Toolshed fully updated with Project Plan preview, unique selections & searchable database!")