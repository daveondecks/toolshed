import streamlit as st

# Set page configuration
st.set_page_config(layout='wide')

# Sidebar with PDCA Expanders (only visible on the main page)
if 'selected_tab' not in st.session_state:
    st.session_state['selected_tab'] = 'Tool Shed'

if st.session_state['selected_tab'] == 'Tool Shed':
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

# Main page with tabs
st.title("Tool Shed")

tab_selection = st.tabs(["Tool Shed", "Tool Dictionary", "Video Library"])

if tab_selection[0]:
    st.session_state['selected_tab'] = 'Tool Shed'
    st.header("🛠️ Welcome to the Tool Shed")
    st.write("This section contains tools and resources for CI (Continuous Improvement).")

elif tab_selection[1]:
    st.session_state['selected_tab'] = 'Tool Dictionary'
    st.write("")  # Blank page

elif tab_selection[2]:
    st.session_state['selected_tab'] = 'Video Library'
    st.write("")  # Blank page

# --- Existing functionality from toolshed.py ---
# (Insert the remaining logic and features of your toolshed.py application here)
