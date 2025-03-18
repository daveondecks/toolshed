
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

# ✅ Store Project Name & Owner in session state
if "project_name" not in st.session_state:
    st.session_state["project_name"] = ""

if "project_owner" not in st.session_state:
    st.session_state["project_owner"] = ""

# ✅ Save inputs to session state (NO DUPLICATE `text_input`)
st.session_state["project_name"] = st.sidebar.text_input("Project Name", value=st.session_state["project_name"])
st.session_state["project_owner"] = st.sidebar.text_input("Project Owner", value=st.session_state["project_owner"])
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

    # ✅ Retrieve selected tools from session state
    selected_tools = st.session_state.selected_tools

    # ✅ Create PDCA toolboxes with colors
    toolbox_cols = st.columns(4)
    for idx, phase in enumerate(["Plan", "Do", "Check", "Act"]):
        with toolbox_cols[idx]:
            tools = selected_tools[phase]
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

            # ✅ Display selected tools
            if not tools:
                st.markdown(f"""
                <div style="
                    background-color: #F1F1F1; 
                    padding: 10px; 
                    border-radius: 5px;
                    text-align: center;
                    margin-top: 5px;
                    color: black;">
                    No tools selected
                </div>
                """, unsafe_allow_html=True)
            else:
                toolbox_html = f"""
                <div style="
                    background-color: white;
                    border: 2px solid {box_color};
                    border-radius: 10px;
                    padding: 10px;
                    margin-top: 5px;
                ">
                <ul style="list-style-type: none; padding: 0;">
                """
                for tool in tools:
                    toolbox_html += f'<li style="padding: 5px; border-bottom: 1px solid {box_color};">✅ {tool}</li>'
                toolbox_html += "</ul></div>"

                st.markdown(toolbox_html, unsafe_allow_html=True)

# === Tool Dictionary Tab ===
with tab2:
    st.subheader("Tool Dictionary")
    
    # Search box
    query = st.text_input("🔍 Search tools:", "")

    # ✅ Case-insensitive filtering
    if query:
        mask = tool_data['Tool Name'].str.contains(query, case=False, na=False) | tool_data['Description'].str.contains(query, case=False, na=False)
        filtered_data = tool_data[mask].copy()
    else:
        filtered_data = tool_data.copy()

    # ✅ Convert 'Tool Name' into clickable links
    if 'More Info' in filtered_data.columns:
        filtered_data['Tool Name'] = filtered_data.apply(
            lambda row: f"<a href='{row['More Info']}' target='_blank'>{row['Tool Name']}</a>" 
                        if pd.notna(row['More Info']) and str(row['More Info']).strip() != "" 
                        else row['Tool Name'],
            axis=1
        )

    # ✅ Display table with same width as the search box
    dict_display = filtered_data[['PDCA Category', 'Tool Name', 'Description']].copy()
    dict_display.rename(columns={'PDCA Category': 'Phase'}, inplace=True)

    if dict_display.empty:
        st.warning("⚠️ No tools found. Try a different search term.")
    else:
        st.container()  # Wrap table inside a container
        st.dataframe(dict_display, use_container_width=True)

# === Video Library Tab ===
with tab3:
    st.subheader("🎥 Video Library - Work in Progress 🚧")
    
    # Work in Progress message with an icon
    st.markdown(
        """
        🚀 **Coming Soon!** This is where you will be able to **upload a short video of your project**.  
        
        🎯 **What to Include in Your Video:**
        - 🎬 A brief **introduction to your project**  
        - 🛠️ The **PDCA tools** you used  
        - 📊 **How successful it was** and **what you learned**  
        - 💡 **Tips for others** who may want to try similar tools  

        🔍 You will also be able to **search videos by PDCA category and keyword**.  

        🏗️ **Just watch this space!** 🎥
        """,
        unsafe_allow_html=True
    )
    # === Project Plan Tab ===
with tab4:
    st.subheader("Project Plan")

    # ✅ Retrieve project details from session state
    project_name = st.session_state["project_name"]
    project_owner = st.session_state["project_owner"]
    created_date = st.session_state.get("created_date", date.today().strftime("%d-%m-%Y"))

    # ✅ Display Project Details
    st.markdown(f"**Project Name:** {project_name} &nbsp;&nbsp; **Owner:** {project_owner} &nbsp;&nbsp; **Created:** {created_date}", unsafe_allow_html=True)
    st.write("")  # Empty line for spacing

    # ✅ Introductory text for the project plan table
    st.write("The table below outlines the selected tools as tasks in your PDCA project plan.")

    # ✅ Add missing tool descriptions
    all_tasks = []
    for phase in ["Plan", "Do", "Check", "Act"]:
        for tool in st.session_state.selected_tools[phase]:
            desc = tool_data.loc[tool_data["Tool Name"] == tool, "Description"].values
            desc_text = desc[0] if len(desc) > 0 else ""
            all_tasks.append({"PDCA Phase": phase, "Task Name": tool, "Description": desc_text})

    project_plan_df = pd.DataFrame(all_tasks)

    # ✅ Display project plan table
    st.dataframe(project_plan_df, use_container_width=True)

    # ✅ Download buttons
    st.markdown("**Download Project Plan:**")
    dcol1, dcol2, dcol3, dcol4 = st.columns(4)

    # ✅ CSV Download
    csv_data = project_plan_df.to_csv(index=False, encoding='utf-8-sig')
    dcol1.download_button("Download CSV", data=csv_data, file_name="Project_Plan.csv", mime="text/csv")
    # ✅ TXT Download
    text_data = project_plan_df.to_csv(index=False, sep='\t')
    dcol3.download_button("Download TXT", data=text_data, file_name="Project_Plan.txt", mime="text/plain")

    # ✅ Excel Download using `xlsxwriter`
try:
    excel_output = io.BytesIO()
    with pd.ExcelWriter(excel_output, engine='xlsxwriter') as writer:
        project_plan_df.to_excel(writer, index=False, sheet_name="Project Plan")
        excel_data = excel_output.getvalue()
    dcol2.download_button("Download Excel", data=excel_data, file_name="Project_Plan.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
except Exception as e:
        dcol2.write("⚠️ Excel export not available")
    
try:
    from fpdf import FPDF
except ImportError:
    FPDF = None

if FPDF is not None:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # ✅ Title Section
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Project Plan - {st.session_state.get('project_name', 'Untitled')}", ln=1, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Owner: {st.session_state.get('project_owner', 'N/A')}    Created: {st.session_state.get('created_date', 'N/A')}", ln=1, align='C')
    pdf.ln(10)

    # ✅ Write tasks to PDF
    if not project_plan_df.empty:
        for _, row in project_plan_df.iterrows():
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 8, f"{row['PDCA Phase']} Phase", ln=1)
            pdf.set_font("Arial", '', 12)

            # ✅ Handle encoding issues
            task_name = row['Task Name'] if row['Task Name'] else "Unnamed Task"
            description = row['Description'] if row['Description'] else "No Description Available"

            def clean_text(text):
                return ''.join(c for c in text if ord(c) < 128)  # Keep only ASCII characters

            task_name = clean_text(task_name)
            description = clean_text(description)

            pdf.cell(0, 6, f"{task_name} - {description}", ln=1)
            pdf.cell(0, 6, "Start Date: ______    Completion Date: ______", ln=1)
            pdf.ln(4)

    else:
        pdf.set_font("Arial", 'I', 12)
        pdf.cell(0, 10, "No tasks selected for this project plan.", ln=1, align='C')

    # ✅ Generate PDF Download Button
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    dcol4.download_button("Download PDF", data=pdf_bytes, file_name="Project_Plan.pdf", mime="application/pdf")

else:
    dcol4.write("⚠️ PDF export not available (FPDF not installed)")

import streamlit as st

# Horizontal top navigation bar
top_nav = st.radio("Navigation", 
                   ["🛠 Toolshed", "📖 Tool Dictionary", "📹 Video Library", "📑 Project Plan", "📊 Analytics", "📂 Repository"], 
                   horizontal=True)

if top_nav == "🛠 Toolshed":
    st.title("🛠 Toolshed")
    st.write("Select tools from each PDCA phase in the sidebar. They will appear in the corresponding toolbox below.")

    # Existing PDCA Toolbox UI elements
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("🟡 Plan Toolbox")
        st.write("No tools selected")
    with col2:
        st.button("🟢 Do Toolbox")
        st.write("No tools selected")
    with col3:
        st.button("🔵 Check Toolbox")
        st.write("No tools selected")
    with col4:
        st.button("🔴 Act Toolbox")
        st.write("No tools selected")

elif top_nav == "📖 Tool Dictionary":
    st.title("📖 Tool Dictionary")
    st.write("Find detailed information about different tools available in the toolshed.")

elif top_nav == "📹 Video Library":
    st.title("📹 Video Library")
    st.write("Access instructional and project-related videos.")

elif top_nav == "📑 Project Plan":
    st.title("📑 Project Plan")
    st.write("Manage your continuous improvement project plans here.")

elif top_nav == "📊 Analytics":
    st.title("📊 Tools Analytics")
    st.write("Analyze tool usage trends and track persistent tool usage.")
    st.info("🔍 Future updates will include AI-based recommendations for the best and most popular tools.")
    
    # Placeholder for analytics features
    st.write("📈 **Upcoming Features:**")
    st.write("- Tool usage trends over time")
    st.write("- AI-based recommendations for best tools")
    st.write("- Predictive maintenance insights")

elif top_nav == "📂 Repository":
    st.title("📂 CI Repository")
    st.write("Upload and share useful CI files with other users.")
    st.warning("🚀 This feature is currently under development and will be available in future updates.")
    
    # Placeholder for file upload section
    st.file_uploader("Upload CI Files", type=["csv", "xlsx", "docx", "pdf"])
    st.write("📁 **Upcoming Features:**")
    st.write("- User-shared files repository")
    st.write("- Categorization and tagging of files")
    st.write("- Access control and permissions")
