import streamlit as st

# Set page configuration
st.set_page_config(layout='wide')

# Define tabs
tab_names = ["Tool Shed", "Tool Dictionary", "Video Library"]
selected_tab = st.radio("Select a tab:", tab_names, horizontal=True)

# Tool Shed page with sidebar expanders
if selected_tab == "Tool Shed":
    with st.sidebar:
        with st.expander("📌 Plan"):
            st.write("Content for the Plan section.")
            st.write("Add relevant tools and guidance for planning.")
        with st.expander("🛠️ Do"):
            st.write("Content for the Do section.")
            st.write("Include execution steps and best practices.")
        with st.expander("✅ Check"):
            st.write("Content for the Check section.")
            st.write("Provide monitoring and evaluation criteria.")
        with st.expander("🚀 Act"):
            st.write("Content for the Act section.")
            st.write("Suggest improvements and corrective actions.")

    # Main content for Tool Shed
    st.title("Tool Shed")
    st.header("🛠️ Welcome to the Tool Shed")
    st.write("This section contains tools and resources for CI (Continuous Improvement).")

# Tool Dictionary (Blank Page, No Sidebar)
elif selected_tab == "Tool Dictionary":
    st.sidebar.empty()  # Hide sidebar
    st.title("Tool Dictionary")
    st.write("")  # Blank page

# Video Library (Blank Page, No Sidebar)
elif selected_tab == "Video Library":
    st.sidebar.empty()  # Hide sidebar
    st.title("Video Library")
    st.write("")  # Blank page

# --- Existing functionality from toolshed.py ---
# (Insert the remaining logic and features of your toolshed.py application here)
