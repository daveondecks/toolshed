import streamlit as st
import pandas as pd
from datetime import date

# Set wide layout for better display of four columns side by side
st.set_page_config(page_title="PDCA Toolshed", layout="wide")

# --- Load tool data from CSV, using caching for performance ---
@st.cache_data
def load_data():
    """Load tools data from CSV file."""
    try:
        # Try loading from 'data' subdirectory (as in repo structure)
        return pd.read_csv("Data/Tools_description.csv")
    except FileNotFoundError:
        # Fallback to current directory if data folder is not present
        return pd.read_csv("Tools_description.csv")

tool_data = load_data()
# Rename unnamed columns to proper labels for ease of use
tool_data = tool_data.rename(columns={
    "Unnamed: 3": "More Info",
    "Unnamed: 4": "Video1",
    "Unnamed: 5": "Video2",
    "Unnamed: 6": "Video3"
})

# --- Sidebar: Project details and tool selection for each PDCA category ---
st.sidebar.title("Project Details")
project_name = st.sidebar.text_input("Project Name")
project_owner = st.sidebar.text_input("Project Owner")
# Store created date on first run
if "created_date" not in st.session_state:
    st.session_state["created_date"] = date.today().strftime("%Y-%m-%d")
created_date = st.session_state["created_date"]

st.sidebar.markdown("---")  # separator line

st.sidebar.header("Select Tools for PDCA Phases")
# Dynamically populate tool options for each phase from the CSV, ensuring unique lists per category
plan_options = tool_data[tool_data['PDCA Category'] == 'Plan']['Tool Name'].tolist()
do_options   = tool_data[tool_data['PDCA Category'] == 'Do']['Tool Name'].tolist()
check_options= tool_data[tool_data['PDCA Category'] == 'Check']['Tool Name'].tolist()
act_options  = tool_data[tool_data['PDCA Category'] == 'Act']['Tool Name'].tolist()

# Multi-select widgets for each PDCA phase (no default selection, user can choose multiple or none)
selected_plan  = st.sidebar.multiselect("Plan Tools:", plan_options)
selected_do    = st.sidebar.multiselect("Do Tools:", do_options)
selected_check = st.sidebar.multiselect("Check Tools:", check_options)
selected_act   = st.sidebar.multiselect("Act Tools:", act_options)

# --- Main interface with tabs ---
st.title("🧰 Continuous Improvement Toolshed")

# Create top-level tabs
tab1, tab2, tab3, tab4 = st.tabs(["Toolshed", "Tool Dictionary", "Video Library", "Project Plan"])

# === Toolshed Tab ===
with tab1:
    st.subheader("Toolshed")
    st.write("Select tools from each PDCA phase in the sidebar. They will appear in the corresponding toolbox below:")
    
    # PDCA step descriptions (to show in expanders above each toolbox column)
    descriptions = {
        "Plan":  "Plan: Define objectives and processes needed to deliver results.",
        "Do":    "Do: Implement the plan and execute the process on a small scale.",
        "Check": "Check: Monitor and evaluate the results against the expected outcomes.",
        "Act":   "Act: Apply learning to adjust the process, and standardize improvements."
    }
    # Display four expanders side by side, one for each PDCA phase description
    exp_cols = st.columns(4)
    for i, phase in enumerate(["Plan", "Do", "Check", "Act"]):
        with exp_cols[i].expander(f"{phase}", expanded=False):
            st.write(descriptions[phase])
    
    # Display four toolbox containers (one per PDCA phase) with curved tops and slots for selected tools
    toolbox_cols = st.columns(4)
    phase_names = ["Plan", "Do", "Check", "Act"]
    selections = [selected_plan, selected_do, selected_check, selected_act]
    for idx, phase in enumerate(phase_names):
        tools = selections[idx]
        # Construct HTML for the toolbox with a curved top border
        toolbox_html = f"""
        <div style="
            background-color: #F1F1F1;
            border: 2px solid #555;
            border-top-left-radius: 10px;
            border-top-right-radius: 10px;
            padding: 10px;
            min-height: 120px;
        ">
        """
        if tools:
            # List each selected tool as a "slot" in the toolbox
            toolbox_html += '<ul style="list-style-type: none; margin: 0; padding-left: 8px;">'
            for j, tool in enumerate(tools):
                # Add a bottom border for each tool slot except the last one to visually separate slots
                border_style = "border-bottom: 1px solid #ccc;" if j < len(tools) - 1 else ""
                toolbox_html += f'<li style="padding: 4px; {border_style}">{tool}</li>'
            toolbox_html += "</ul>"
        else:
            # If no tool selected for this phase, indicate an empty toolbox
            toolbox_html += '<em>No tools selected</em>'
        toolbox_html += "</div>"
        # Render the toolbox HTML in the respective column
        toolbox_cols[idx].markdown(toolbox_html, unsafe_allow_html=True)

# === Tool Dictionary Tab ===
with tab2:
    st.subheader("Tool Dictionary")
    st.write("Browse and search for tools. Click on a tool name to learn more (if link is available).")
    
    # Search box for filtering tools by name or description
    query = st.text_input("Search tools:", "")
    if query:
        # Case-insensitive substring match in Tool Name or Description
        mask = tool_data['Tool Name'].str.contains(query, case=False, na=False) | tool_data['Description'].str.contains(query, case=False, na=False)
        filtered_data = tool_data[mask].copy()
    else:
        filtered_data = tool_data.copy()
    
    # Convert 'Tool Name' into clickable link if a 'More Info' URL is provided for that tool
    if 'More Info' in filtered_data.columns:
        # Create HTML anchor tags for tool names that have a link, otherwise just use the name
        filtered_data['Tool Name'] = filtered_data.apply(
            lambda row: f"<a href='{row['More Info']}' target='_blank'>{row['Tool Name']}</a>" 
                        if pd.notna(row['More Info']) and str(row['More Info']).strip() != "" 
                        else row['Tool Name'],
            axis=1
        )
    # Select columns to display
    dict_display = filtered_data[['PDCA Category', 'Tool Name', 'Description']].copy()
    dict_display.rename(columns={'PDCA Category': 'Phase'}, inplace=True)
    # If no results, display a message; otherwise display the table of tools
    if dict_display.empty:
        st.write("No tools found. Try a different search term.")
    else:
        # Display the filtered tool list as an HTML table with clickable links (if any)
        st.markdown(dict_display.to_html(escape=False, index=False), unsafe_allow_html=True)

# === Video Library Tab ===
with tab3:
    st.subheader("Video Library")
    st.write("Explore video resources for continuous improvement tools, organized by PDCA phase.")
    # Iterate through each phase and list videos if available
    for phase in ["Plan", "Do", "Check", "Act"]:
        phase_tools = tool_data[tool_data['PDCA Category'] == phase]
        st.markdown(f"**{phase} Phase**", unsafe_allow_html=True)
        videos_found = False
        for _, row in phase_tools.iterrows():
            # Gather all video links for this tool (Video1, Video2, Video3 columns)
            video_links = []
            for col in ['Video1', 'Video2', 'Video3']:
                if col in row and pd.notna(row[col]) and str(row[col]).strip() != "":
                    video_links.append(row[col])
            if video_links:
                videos_found = True
                st.markdown(f"*{row['Tool Name']}*")
                for link in video_links:
                    # Embed each video link. Streamlit will auto-render YouTube links or video URLs.
                    st.video(link)
        if not videos_found:
            st.write("*(No video resources available for this phase.)*")

# === Project Plan Tab ===
with tab4:
    st.subheader("Project Plan")
    # Display project name, owner, and created date at the top in bold
    st.markdown(f"**Project Name:** {project_name if project_name else 'N/A'} &nbsp;&nbsp; **Owner:** {project_owner if project_owner else 'N/A'} &nbsp;&nbsp; **Created:** {created_date}", unsafe_allow_html=True)
    st.write("")  # empty line for spacing
    
    # Introductory text for the project plan table
    st.write("The table below outlines the selected tools as tasks in your PDCA project plan. You can fill in the start and completion dates after downloading the plan.")
    
    # Define background colors for each phase section in the plan
    phase_colors = {
        "Plan":  "#cce5ff",  # light blue
        "Do":    "#d4edda",  # light green
        "Check": "#fff3cd",  # light yellow
        "Act":   "#f8d7da"   # light red/pink
    }
    # Build and display a table for each phase with selected tools
    for phase, color in phase_colors.items():
        # Determine selected tools for this phase
        if phase == "Plan":
            tools_list = selected_plan
        elif phase == "Do":
            tools_list = selected_do
        elif phase == "Check":
            tools_list = selected_check
        else:  # "Act"
            tools_list = selected_act
        if not tools_list:
            continue  # skip this phase if no tools selected
        
        # Section header with colored background for the phase
        st.markdown(f"<div style='background-color: {color}; padding: 6px 8px;'><b>{phase} Phase</b></div>", unsafe_allow_html=True)
        # Create a DataFrame for the selected tools in this phase
        phase_df = tool_data[tool_data['Tool Name'].isin(tools_list)][['Tool Name', 'Description']].copy()
        phase_df.insert(2, 'Start Date', '')        # blank start date column
        phase_df.insert(3, 'Completion Date', '')   # blank completion date column
        phase_df.rename(columns={'Tool Name': 'Task Name'}, inplace=True)
        phase_df = phase_df.reset_index(drop=True)
        # Display the phase task table
        st.table(phase_df)
        st.markdown("<br/>", unsafe_allow_html=True)  # add a small vertical space
    
    # Prepare a combined project plan DataFrame for download (include phase as a column)
    all_tasks = []
    for phase in ["Plan", "Do", "Check", "Act"]:
        if phase == "Plan":
            tools_list = selected_plan
        elif phase == "Do":
            tools_list = selected_do
        elif phase == "Check":
            tools_list = selected_check
        else:
            tools_list = selected_act
        for tool in tools_list:
            # Get description from data
            desc = ""
            if not tool_data[tool_data['Tool Name'] == tool].empty:
                desc = tool_data[tool_data['Tool Name'] == tool]['Description'].values[0]
            all_tasks.append({
                "PDCA Phase": phase,
                "Task Name": tool,
                "Description": desc,
                "Start Date": "",
                "Completion Date": ""
            })
    project_plan_df = pd.DataFrame(all_tasks)
    
    # --- Download buttons for CSV, Excel, PDF, and Text formats ---
    st.markdown("**Download Project Plan:**")
    dcol1, dcol2, dcol3, dcol4 = st.columns(4)
    # CSV download (with BOM for Excel compatibility)
    csv_data = project_plan_df.to_csv(index=False, encoding='utf-8-sig')
    dcol1.download_button("Download CSV", data=csv_data, file_name="Project_Plan.csv", mime="text/csv")
    # Excel download (using xlsxwriter engine)
    try:
        import io
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            project_plan_df.to_excel(writer, index=False, sheet_name="Project Plan")
        excel_data = excel_buffer.getvalue()
        dcol2.download_button("Download Excel", data=excel_data, file_name="Project_Plan.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        # If Excel generation fails (missing module), disable Excel download button
        dcol2.write("Excel export not available")
    # Text download (simple tab-separated text)
    text_data = project_plan_df.to_csv(index=False, sep='\t')
    dcol3.download_button("Download TXT", data=text_data, file_name="Project_Plan.txt", mime="text/plain")
    # PDF download (generate simple PDF using fpdf if available)
    try:
        from fpdf import FPDF
    except ImportError:
        FPDF = None
    pdf_bytes = b""
    if FPDF:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        # Title
        pdf.cell(0, 10, f"Project Plan - {project_name if project_name else 'Untitled'}", ln=1, align='C')
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, f"Owner: {project_owner if project_owner else 'N/A'}    Created: {created_date}", ln=1, align='C')
        pdf.ln(10)
        current_phase = None
        pdf.set_font("Arial", '', 12)
        # Add each task, grouped by phase with section headers
        for _, row in project_plan_df.iterrows():
            phase = row["PDCA Phase"]
            task = row["Task Name"]
            desc = row["Description"]
            if phase != current_phase:
                # New phase section in PDF
                current_phase = phase
                pdf.set_font("Arial", 'B', 14)
                pdf.cell(0, 8, f"{phase} Phase", ln=1)
                pdf.set_font("Arial", '', 12)
            # Task name and description
            task_line = f"{task} - {desc}"
            # Ensure encoding for PDF (FPDF supports Latin-1)
            try:
                task_line = task_line.encode('latin-1', 'ignore').decode('latin-1')
            except Exception:
                task_line = task_line.encode('latin-1', 'replace').decode('latin-1')
            pdf.cell(0, 6, task_line, ln=1)
            # Placeholder for dates
            pdf.cell(0, 6, "Start Date: ______    Completion Date: ______", ln=1)
            pdf.ln(4)
        pdf_bytes = pdf.output(dest='S').encode('latin-1')
        dcol4.download_button("Download PDF", data=pdf_bytes, file_name="Project_Plan.pdf", mime="application/pdf")
    else:
        dcol4.write("PDF export not available")