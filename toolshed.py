import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
from fpdf import FPDF  # Make sure to add `fpdf` to requirements for PDF generation

# Set page configuration for wide layout
st.set_page_config(page_title="PDCA Tool Shed", layout="wide")

# Load tools data from CSV (cached for performance)
@st.cache_data
def load_tools_data():
    return pd.read_csv("Tools_description.csv")

tool_data = load_tools_data().dropna(subset=["Tool Name"])  # drop any rows without a tool name

# Prepare list of tools for each PDCA category
categories = ["Plan", "Do", "Check", "Act"]
tools_by_category = {cat: tool_data[tool_data["PDCA Category"] == cat]["Tool Name"].tolist() 
                     for cat in categories}

# Sidebar: Tool selection for each PDCA phase (ensure unique selections per category)
st.sidebar.header("Select Tools for Project Plan")
selected_tools = {}
for cat in categories:
    selected_tools[cat] = st.sidebar.multiselect(
        f"{cat} Tools", options=tools_by_category.get(cat, []), key=f"select_{cat}"
    )

# Create top-level tabs
tab1, tab2, tab3, tab4 = st.tabs(["Tool Shed", "Tool Dictionary", "Video Library", "Project Plan"])

# 1. Tool Shed Tab
with tab1:
    st.subheader("Tool Shed")
    st.write("Browse improvement tools organized by PDCA phase. Click on a tool to see its description.")
    # Define distinct colors for each PDCA section
    colors = {"Plan": "#3498db", "Do": "#2ecc71", "Check": "#e67e22", "Act": "#e74c3c"}
    # Layout four columns for Plan/Do/Check/Act
    col_plan, col_do, col_check, col_act = st.columns(4)
    for cat, col in zip(categories, [col_plan, col_do, col_check, col_act]):
        with col:
            # Category header with colored background
            col.markdown(
                f"<div style='background-color:{colors[cat]}; padding:5px; text-align:center;'>"
                f"<span style='color:white; font-weight:bold;'>{cat}</span>"
                f"</div>", unsafe_allow_html=True
            )
            # List each tool in this category with an expander for its description
            for tool in tools_by_category.get(cat, []):
                # Find tool description from the dataframe
                desc = ""
                tool_info = tool_data[tool_data["Tool Name"] == tool]
                if not tool_info.empty:
                    desc = str(tool_info.iloc[0]["Description"])
                with st.expander(tool):
                    st.write(desc if desc else "*(No description available)*")

# 2. Tool Dictionary Tab
with tab2:
    st.subheader("Tool Dictionary")
    st.write("Search and explore all tools and their definitions below.")
    # Search input for filtering tools
    query = st.text_input("Search tools by name or keyword:", "")
    if query:
        # Filter tools by name or description (case-insensitive match)
        filtered_data = tool_data[
            tool_data["Tool Name"].str.contains(query, case=False) |
            tool_data["Description"].str.contains(query, case=False)
        ]
    else:
        filtered_data = tool_data
    # Sort the filtered tools alphabetically by name
    filtered_data = filtered_data.sort_values("Tool Name")
    # Display each tool with its category and description in an expander
    for _, row in filtered_data.iterrows():
        tool_name = row["Tool Name"]
        category = row["PDCA Category"]
        description = row["Description"]
        with st.expander(f"{tool_name} ({category})"):
            st.write(description)

# 3. Video Library Tab
with tab3:
    st.subheader("Video Library")
    st.write("Explore video resources for PDCA and continuous improvement tools.")
    # Placeholder content for the video library (to be filled with actual videos/links)
    st.write("*(Video library content coming soon...)*")

# 4. Project Plan Tab
with tab4:
    st.subheader("Project Plan")
    st.write("Enter project details and review selected PDCA tools. You can then download a report.")
    # Input fields for Project Name and Project Owner
    project_name = st.text_input("Project Name:", "")
    project_owner = st.text_input("Project Owner:", "")
    # Capture current date as Date Created
    date_created = datetime.now().strftime("%Y-%m-%d")
    # Display project dates (Date Started/Completed as placeholders)
    st.write(f"**Date Created:** {date_created}")
    st.write("**Date Started:** *(TBD)*")
    st.write("**Date Completed:** *(TBD)*")
    st.markdown("---")
    # Show selected tools by category with colored category labels
    for cat in categories:
        st.markdown(
            f"<div style='background-color:{colors[cat]}; padding:4px; display:inline-block;'>"
            f"<span style='color:white; font-weight:bold;'>{cat}</span>"
            f"</div>", unsafe_allow_html=True
        )
        tools_list = selected_tools.get(cat, [])
        if tools_list:
            for tool in tools_list:
                st.write(f"- {tool}")
        else:
            st.write("*(No tools selected)*")
    # Generate report and download buttons if a project name or owner is provided
    if project_name or project_owner:
        # Build CSV content
        csv_lines = [
            f"Project Name,{project_name}",
            f"Project Owner,{project_owner}",
            f"Date Created,{date_created}",
            "Date Started,",
            "Date Completed,",
            "",
            "Category,Tools Selected"
        ]
        # Build text content
        text_lines = [
            f"Project Name: {project_name}",
            f"Project Owner: {project_owner}",
            f"Date Created: {date_created}",
            "Date Started: ",
            "Date Completed: ",
            ""
        ]
        # Add each category and selected tools to the report content
        for cat in categories:
            tools_list = selected_tools.get(cat, [])
            if tools_list:
                csv_lines.append(f"{cat},{'; '.join(tools_list)}")
                text_lines.append(f"{cat}:")
                for tool in tools_list:
                    text_lines.append(f"  - {tool}")
            else:
                csv_lines.append(f"{cat},None")
                text_lines.append(f"{cat}:")
                text_lines.append("  None")
        csv_content = "\n".join(csv_lines)
        text_content = "\n".join(text_lines)
        # Build Excel content using pandas
        report_rows = [
            {"Field": "Project Name", "Value": project_name},
            {"Field": "Project Owner", "Value": project_owner},
            {"Field": "Date Created", "Value": date_created},
            {"Field": "Date Started", "Value": ""},
            {"Field": "Date Completed", "Value": ""},
            {"Field": "", "Value": ""},  # blank row
            {"Field": "Category", "Value": "Tools Selected"}
        ]
        for cat in categories:
            tools_str = "; ".join(selected_tools.get(cat, [])) if selected_tools.get(cat, []) else "None"
            report_rows.append({"Field": cat, "Value": tools_str})
        report_df = pd.DataFrame(report_rows)
        excel_buffer = BytesIO()
        try:
            with pd.ExcelWriter(excel_buffer, engine="openpyxl") as writer:
                report_df.to_excel(writer, index=False, sheet_name="Project Plan")
        except Exception:
            # Fallback: if openpyxl is not installed, use CSV content for Excel download
            excel_buffer = BytesIO(csv_content.encode("utf-8"))
        excel_data = excel_buffer.getvalue()
        # Build PDF content using fpdf
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, f"Project Plan: {project_name}", ln=True)
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Project Owner: {project_owner}", ln=True)
        pdf.cell(0, 10, f"Date Created: {date_created}", ln=True)
        pdf.cell(0, 10, "Date Started: ", ln=True)
        pdf.cell(0, 10, "Date Completed: ", ln=True)
        pdf.ln(10)
        # Add tools by category in the PDF (with category color formatting)
        for cat in categories:
            # Convert hex color to RGB
            hex_color = colors[cat]
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            pdf.set_text_color(r, g, b)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, f"{cat}:", ln=True)
            pdf.set_text_color(0, 0, 0)
            pdf.set_font("Arial", "", 12)
            tools_list = selected_tools.get(cat, [])
            if tools_list:
                for tool in tools_list:
                    pdf.cell(0, 10, f"  - {tool}", ln=True)
            else:
                pdf.cell(0, 10, "  None", ln=True)
            pdf.ln(5)
        pdf_data = pdf.output(dest="S").encode("latin1")
        # Download buttons for Excel, CSV, PDF, and Text formats
        st.markdown("**Download Project Plan:**")
        dl_col1, dl_col2, dl_col3, dl_col4 = st.columns(4)
        with dl_col1:
            st.download_button("⬇️ Excel", data=excel_data, 
                               file_name=f"{project_name or 'Project'}_Plan.xlsx", 
                               mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        with dl_col2:
            st.download_button("⬇️ CSV", data=csv_content, 
                               file_name=f"{project_name or 'Project'}_Plan.csv", mime="text/csv")
        with dl_col3:
            st.download_button("⬇️ PDF", data=pdf_data, 
                               file_name=f"{project_name or 'Project'}_Plan.pdf", mime="application/pdf")
        with dl_col4:
            st.download_button("⬇️ Text", data=text_content, 
                               file_name=f"{project_name or 'Project'}_Plan.txt", mime="text/plain")