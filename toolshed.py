import streamlit as st
import pandas as pd
import io
import xlsxwriter
from datetime import date

# Set wide layout
st.set_page_config(page_title="PDCA Toolshed", layout="wide")

# ✅ Load tool data
@st.cache_data
def load_data():
    try:
        return pd.read_csv("Data/Tools_description.csv")
    except FileNotFoundError:
        return pd.read_csv("Tools_description.csv")

tool_data = load_data()

# ✅ Fix column names
tool_data = tool_data.rename(columns={
    "Unnamed: 3": "More Info",
    "Unnamed: 4": "Video1",
    "Unnamed: 5": "Video2",
    "Unnamed: 6": "Video3"
})

# ✅ Sidebar: Project Details & PDCA Selection
st.sidebar.title("Project Details")
project_name = st.sidebar.text_input("Project Name")
project_owner = st.sidebar.text_input("Project Owner")

# ✅ Store created date
if "created_date" not in st.session_state:
    st.session_state["created_date"] = date.today().strftime("%d-%m-%Y")
created_date = st.session_state["created_date"]

st.sidebar.markdown("---")  # separator line

st.sidebar.header("Select Tools for PDCA Phases")

# ✅ Ensure session state is initialized properly
if "selected_tools" not in st.session_state:
    st.session_state.selected_tools = {
        "Plan": [],
        "Do": [],
        "Check": [],
        "Act": []
    }

# ✅ Unified PDCA Selection (Used in Both Toolshed & Project Plan Tabs)
for phase in ["Plan", "Do", "Check", "Act"]:
    selected_temp = st.sidebar.multiselect(
        f"{phase} Tools:",
        options=tool_data[tool_data['PDCA Category'] == phase]['Tool Name'].tolist(),
        default=st.session_state.selected_tools.get(phase, [])
    )

    # ✅ Update session state if selection changes
    if selected_temp != st.session_state.selected_tools[phase]:
        st.session_state.selected_tools[phase] = selected_temp

# ✅ Define PDCA colors (matching your screenshot)
pdca_colors = {
    "Plan": "#FFD700",  # Gold Yellow
    "Do": "#32CD32",    # Green
    "Check": "#1E90FF", # Blue
    "Act": "#FF4500"    # Red
}

# ✅ Main Tabs
st.title("🧰 One Team Continuous Improvement Toolshed")
tab1, tab2, tab3, tab4 = st.tabs(["Toolshed", "Tool Dictionary", "Video Library", "Project Plan"])

# === Toolshed Tab ===
with tab1:
    st.subheader("Toolshed")
    st.write("Select tools from each PDCA phase in the sidebar. They will appear in the corresponding toolbox below:")

    # ✅ PDCA Descriptions
    descriptions = {
        "Plan": """📌 **Description:** The **Plan** phase focuses on identifying problems, analyzing root causes, and planning improvements.  
        🛠 **Tools:** 5 Whys, Fishbone Diagram, SWOT, SMART Goals  
        ✅ **Best Practices:** Use data, involve stakeholders, keep objectives clear  
        ⚠️ **Mistakes:** Skipping root cause analysis, vague goals, poor stakeholder engagement""",

        "Do": """📌 **Description:** The **Do** phase involves implementing the planned solutions on a small scale.  
        🛠 **Tools:** Pilot Testing, SOPs, Training, Gantt Charts  
        ✅ **Best Practices:** Test before full rollout, train employees, track progress  
        ⚠️ **Mistakes:** Lack of training, too many changes at once, ignoring feedback""",

        "Check": """📌 **Description:** The **Check** phase reviews results and compares them with expected outcomes.  
        🛠 **Tools:** KPI Tracking, Control Charts, Pareto Analysis  
        ✅ **Best Practices:** Review objectively, involve the team, use both qualitative & quantitative data  
        ⚠️ **Mistakes:** No KPIs set, ignoring feedback, assuming success without checking""",

        "Act": """📌 **Description:** The **Act** phase determines whether changes should be standardized or modified.  
        🛠 **Tools:** SOP Updates, Training Plans, Lessons Learned  
        ✅ **Best Practices:** Document changes, communicate improvements, continue PDCA cycle  
        ⚠️ **Mistakes:** No documentation, no training follow-up, assuming process is fixed"""
    }

    # ✅ PDCA Expanders
    exp_cols = st.columns(4)
    for i, phase in enumerate(["Plan", "Do", "Check", "Act"]):
        with exp_cols[i].expander(f"{phase}", expanded=False):
            st.markdown(descriptions[phase])

    # ✅ Display PDCA Toolboxes
    toolbox_cols = st.columns(4)
    for idx, phase in enumerate(["Plan", "Do", "Check", "Act"]):
        with toolbox_cols[idx]:
            tools = st.session_state.selected_tools[phase]
            box_color = pdca_colors[phase]

            # ✅ Render PDCA-colored Toolbox Header
            st.markdown(f"""
            <div style="
                background-color: {box_color}; 
                padding: 15px; 
                border-radius: 10px; 
                text-align: center; 
                color: white; 
                font-weight: bold;">
                {phase} Toolbox
            </div>
            """, unsafe_allow_html=True)

            # ✅ Display tools or "No tools selected"
            if not tools:
                st.markdown(f"""
                <div style="background-color: #F1F1F1; padding: 10px; border-radius: 5px; text-align: center; margin-top: 5px; color: black;">
                No tools selected
                </div>
                """, unsafe_allow_html=True)
            else:
                toolbox_html = f"""
                <div style="background-color: white; border: 2px solid {box_color}; border-radius: 10px; padding: 10px; margin-top: 5px;">
                <ul style="list-style-type: none; padding: 0;">
                """
                for tool in tools:
                    toolbox_html += f'<li style="padding: 5px; border-bottom: 1px solid {box_color};">✅ {tool}</li>'
                toolbox_html += "</ul></div>"

                st.markdown(toolbox_html, unsafe_allow_html=True)

# === Project Plan Tab ===
with tab4:
    st.subheader("Project Plan")
    st.write("The table below outlines the selected tools as tasks in your PDCA project plan.")

    # ✅ Display table
    all_tasks = [{"PDCA Phase": phase, "Task Name": tool, "Description": ""} for phase in ["Plan", "Do", "Check", "Act"] for tool in st.session_state.selected_tools[phase]]
    project_plan_df = pd.DataFrame(all_tasks)
    st.dataframe(project_plan_df, use_container_width=True)

    # ✅ Download buttons
    st.write("Download Project Plan:")
    st.download_button("Download CSV", project_plan_df.to_csv(index=False), "project_plan.csv", "text/csv")
    st.download_button("Download TXT", project_plan_df.to_csv(index=False, sep="\t"), "project_plan.txt", "text/plain")