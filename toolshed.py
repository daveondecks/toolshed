import streamlit as st
import pandas as pd
import datetime

# Set page configuration
st.set_page_config(layout="wide")

# Load CSV data
@st.cache_data
def load_data():
    return pd.read_csv("Data/Tools_description.csv")

tool_data = load_data()

# Sidebar PDCA selection
pdca_steps = {
    "Plan": ["MoSCoW", "Five Ys", "VSM", "Flow Chart", "Six S’s", "Process Map", "DMAIC", "RACI", "Route Cause", "VOC"],
    "Do": ["Gemba", "Kaizen", "SPC", "Kanban", "Pareto Chart", "Regression", "Poka-yoke", "SIPOC", "FMEA", "Asana"],
    "Check": ["Control Charts", "Check sheet", "Dashboard", "X-Matrix", "Heat Map", "Estimation", "DPMO", "Benchmarking", "Discovery", "Testing"],
    "Act": ["Deployment", "Quality", "Time", "Comms", "TQM", "Standard Work", "Lessons", "Risk Matrix", "Stakeholders", "Change Mgt"]
}

selected_tools = {step: [] for step in pdca_steps}

# Function to ensure unique tool selection
def unique_selectbox(label, options, key, selected_options):
    available_options = [option for option in options if option not in selected_options]
    if not available_options:
        st.warning("All tools in this section have been selected. Please choose different tools.")
        return None
    selection = st.selectbox(label, available_options, key=key)
    selected_options.append(selection)
    return selection

# Sidebar UI
with st.sidebar:
    for step, tools in pdca_steps.items():
        with st.expander(f"📌 {step}"):
            st.markdown(f"### {step} Tools")
            selected_tools[step] = [
                unique_selectbox(f"Select a {step} tool", tools, f"{step.lower()}1", selected_tools[step]),
                unique_selectbox(f"Select another {step} tool", tools, f"{step.lower()}2", selected_tools[step]),
                unique_selectbox(f"Select one more {step} tool", tools, f"{step.lower()}3", selected_tools[step])
            ]

# Main Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🛠️ Tool Shed", "📖 Tool Dictionary", "📺 Video Library", "📄 Project Plan"])

# Tool Shed Tab
with tab1:
    st.header("🛠️ Tool Shed")
    st.write("This section provides a collection of tools for Continuous Improvement (CI).")

# Tool Dictionary Tab
with tab2:
    st.header("📖 Tool Dictionary")
    st.write("Search and explore CI tools with descriptions and links.")
    search_query = st.text_input("🔍 Search for a tool:")
    filtered_data = tool_data[tool_data["Tool Name"].str.contains(search_query, case=False, na=False)]
    
    # Convert tool names into clickable links
    filtered_data["Tool Name"] = filtered_data.apply(
        lambda row: f"[{row['Tool Name']}]({row['More Info']})" if pd.notna(row["More Info"]) else row["Tool Name"],
        axis=1
    )
    
    # Display searchable table with full width
    st.dataframe(filtered_data[['Tool Name', 'PDCA Category', 'Description']], width=1500)

# Project Plan Tab
with tab4:
    st.header("📄 Project Plan Preview")
    project_name = st.text_input("Project Name")
    project_owner = st.text_input("Project Owner")
    date_created = datetime.datetime.now().strftime("%Y-%m-%d")

    plan_data = []
    for step, tools in selected_tools.items():
        for tool in tools:
            if tool:
                tool_info = tool_data[tool_data["Tool Name"] == tool]
                description = tool_info["Description"].values[0] if not tool_info.empty else "N/A"
                plan_data.append([step, tool, description, "", ""])  # Placeholder for Date Started & Completed

    # Convert to DataFrame and display
    plan_df = pd.DataFrame(plan_data, columns=["PDCA Step", "Tool", "Description", "Date Started", "Date Completed"])
    st.dataframe(plan_df, width=1500)

    # Download Project Plan
    if not plan_df.empty:
        csv = plan_df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download Project Plan", csv, "Project_Plan.csv", "text/csv")

# Success Message
st.success("🚀 Toolshed fully updated with Project Plan preview, unique selections & searchable database!")
