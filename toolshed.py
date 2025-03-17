import streamlit as st
import pandas as pd
from datetime import date

# Set wide layout for better display of four columns side by side
st.set_page_config(page_title="One Team Continuous Improvement Toolshed", layout="wide")

# --- Load tool data from CSV, using caching for performance ---
@st.cache_data
def load_data():
    """Load tools data from CSV file."""
    try:
        # Try loading from 'data' subdirectory (as in repo structure)
        return pd.read_csv("Data/Tools_description.csv")
    except FileNotFoundError:
        # Fallback to current directory if data folder is not present
        return pd.read_csv("Data/Tools_description.csv")

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
project_name = st.sidebar.text_input("Project Name", "")

# Define PDCA step colors
pdca_colors = {
    "Plan": "#FFD700",  # Gold
    "Do": "#32CD32",  # Lime Green
    "Check": "#1E90FF",  # Dodger Blue
    "Act": "#FF4500"  # Orange Red
}

# PDCA Expanders with additional sections
for step, color in pdca_colors.items():
    with st.expander(f"{step} - {step} Stage", expanded=False):
        st.markdown(f'<div style="background-color:{color}; padding:10px; border-radius:5px;">', unsafe_allow_html=True)
        st.subheader(f"{step} Phase")
        st.write("### Description")
        st.write(f"This is the {step} phase of PDCA where you...")
        st.write("### Examples of Tools")
        st.write("- Example tool 1\n- Example tool 2\n- Example tool 3")
        st.write("### Best Practices")
        st.write("- Best practice 1\n- Best practice 2\n- Best practice 3")
        st.write("### Typical Mistakes")
        st.write("- Mistake 1\n- Mistake 2\n- Mistake 3")
        st.markdown('</div>', unsafe_allow_html=True)

# Full-width Tool Dictionary Table
st.subheader("Tool Dictionary Table")
st.markdown('<style>div[data-testid="stTable"]{width:100% !important;}</style>', unsafe_allow_html=True)

# Remove Excel button and keep three download options
st.download_button("Download CSV", "", "toolshed.csv")
st.download_button("Download PDF", "", "toolshed.pdf")
st.download_button("Download JSON", "", "toolshed.json")

# Project Plan PDCA Section with dividers
st.markdown("## Project Plan - PDCA Breakdown")
st.markdown("---")
for step, color in pdca_colors.items():
    st.markdown(f'<div style="background-color:{color}; padding:10px; border-radius:5px;">', unsafe_allow_html=True)
    st.subheader(f"{step} Phase")
    st.write(f"Detailed breakdown of the {step} phase in project planning.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")
