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

# === Tool Dictionary Tab ===
with tab2:
    st.subheader("Tool Dictionary")
    st.write("Browse and search for tools. Click on a tool name to learn more (if link is available).")

    # ✅ Ensure tool dictionary is displayed correctly
    query = st.text_input("Search tools:", "")
    if query:
        # ✅ Case-insensitive filtering
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

    # ✅ Display tool dictionary table
    dict_display = filtered_data[['PDCA Category', 'Tool Name', 'Description']].copy()
    dict_display.rename(columns={'PDCA Category': 'Phase'}, inplace=True)

    if dict_display.empty:
        st.write("No tools found. Try a different search term.")
    else:
        st.markdown(dict_display.to_html(escape=False, index=False), unsafe_allow_html=True)

# === Project Plan Tab ===
with tab4:
    st.subheader("Project Plan")
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

    # ✅ PDF Download (Re-Added)
    try:
        from fpdf import FPDF
    except ImportError:
        FPDF = None

    if FPDF:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, f"Project Plan - {project_name if project_name else 'Untitled'}", ln=1, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Owner: {project_owner if project_owner else 'N/A'}    Created: {created_date}", ln=1, align='C')
        pdf.ln(10)

        for _, row in project_plan_df.iterrows():
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 8, f"{row['PDCA Phase']} Phase", ln=1)
            pdf.set_font("Arial", '', 12)
            pdf.cell(0, 6, f"{row['Task Name']} - {row['Description']}", ln=1)
            pdf.cell(0, 6, "Start Date: ______    Completion Date: ______", ln=1)
            pdf.ln(4)

        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        dcol4.download_button("Download PDF", data=pdf_bytes, file_name="Project_Plan.pdf", mime="application/pdf")
    else:
        dcol4.write("PDF export not available")