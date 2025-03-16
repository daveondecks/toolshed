import streamlit as st
import pandas as pd
import datetime

# Set page configuration
st.set_page_config(layout="wide")

# Load CSV data
@st.cache_data
def load_data():
    return pd.read_csv("data/Tools_description.csv")

tool_data = load_data()

# Function to ensure unique tool selection within each PDCA section
def unique_selectbox(label, options, key, selected_options):
    available_options = [option for option in options if option not in selected_options]
    if not available_options:
        st.warning("All tools in this section have been selected. Please choose different tools.")
        return None
    selection = st.selectbox(label, available_options, key=key)
    selected_options.append(selection)
    return selection

# Sidebar with tool selection
st.sidebar.header("PDCA Tool Selection")
selected_tools = {"Plan": [], "Do": [], "Check": [], "Act": []}

for category in selected_tools.keys():
    with st.sidebar.expander(f"{category} Tools", expanded=False):
        category_tools = tool_data[tool_data['PDCA Category'] == category]['Tool Name'].tolist()
        for i in range(3):
            unique_selectbox(f"Select {category} tool {i+1}", category_tools, f"{category.lower()}_{i}", selected_tools[category])

# Main Page Tabs
tab1, tab2, tab3, tab4 = st.tabs(["⚒️ Tool Shed", "📖 Tool Dictionary", "🎥 Video Library", "📄 Project Plan"])

with tab1:
    st.header("⚒️ Tool Shed")
    st.success("🚀 Toolshed fully updated with Project Plan preview, unique selections & searchable database!")

with tab2:
    st.header("📖 Tool Dictionary")
    st.write("Search and explore CI tools with descriptions and links.")
    search_query = st.text_input("🔍 Search for a tool:")
    filtered_data = tool_data[tool_data['Tool Name'].str.contains(search_query, case=False, na=False)]
    
    # Convert tool name into clickable links
    filtered_data['Tool Name'] = filtered_data.apply(
        lambda row: f"[{row['Tool Name']}]({row['More Info']})" if pd.notna(row['More Info']) else row['Tool Name'], axis=1)
    
    # Display searchable table
    st.dataframe(filtered_data[['Tool Name', 'PDCA Category', 'Description']], use_container_width=True)

with tab3:
    st.header("🎥 Video Library")
    st.write("Coming Soon...")

with tab4:
    st.header("📄 Project Plan Preview")
    project_name = st.text_input("Project Name:")
    project_owner = st.text_input("Project Owner:")
    date_created = datetime.datetime.today().strftime('%Y-%m-%d')
    
    project_df = pd.DataFrame({
        "PDCA Stage": [],
        "Selected Tools": [],
        "Description": [],
        "Date Started": [],
        "Date Completed": []
    })
    
    for category, tools in selected_tools.items():
        for tool in tools:
            description = tool_data[tool_data['Tool Name'] == tool]['Description'].values
            project_df = project_df.append({
                "PDCA Stage": category,
                "Selected Tools": tool,
                "Description": description[0] if len(description) > 0 else "",
                "Date Started": "",
                "Date Completed": ""
            }, ignore_index=True)
    
    # Format with colors
    category_colors = {"Plan": "#FFFF66", "Do": "#99CCFF", "Check": "#99FF99", "Act": "#FFCC99"}
    project_df['Color'] = project_df['PDCA Stage'].map(category_colors)
    
    st.dataframe(project_df[['PDCA Stage', 'Selected Tools', 'Description', 'Date Started', 'Date Completed']], use_container_width=True)
    
    # Download options
    st.subheader("Download Project Plan")
    format_option = st.radio("Choose file format:", ["CSV", "Excel", "PDF", "TXT"])
    
    if st.button("Download Plan"):
        if format_option == "CSV":
            project_df.to_csv("Project_Plan.csv", index=False)
            st.download_button(label="Download CSV", data=open("Project_Plan.csv", "rb"), file_name="Project_Plan.csv")
        elif format_option == "Excel":
            project_df.to_excel("Project_Plan.xlsx", index=False)
            st.download_button(label="Download Excel", data=open("Project_Plan.xlsx", "rb"), file_name="Project_Plan.xlsx")
        elif format_option == "PDF":
            project_df.to_string("Project_Plan.pdf")
            st.download_button(label="Download PDF", data=open("Project_Plan.pdf", "rb"), file_name="Project_Plan.pdf")
        elif format_option == "TXT":
            project_df.to_csv("Project_Plan.txt", index=False, sep='\t')
            st.download_button(label="Download TXT", data=open("Project_Plan.txt", "rb"), file_name="Project_Plan.txt")
    
    st.success("📄 Project Plan ready for download!")
