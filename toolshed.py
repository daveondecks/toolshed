import streamlit as st
import pandas as pd

# Define tools under each category
plan_tools = ["MoSCoW", "Five Ys", "VSM", "Flow Chart", "Six S’s", "Process Map", "DMAIC", "RACI", "Route Cause", "VOC"]
do_tools = ["Gemba", "Kaizen", "SPC", "Kanban", "Pareto Chart", "Regression", "Poka-yoke", "SIPOC", "FMEA", "Asana"]
check_tools = ["Control Charts", "Check sheet", "Dashboard", "X-Matrix", "Heat Map", "Estimation", "DPMO", "Benchmarking", "Discovery", "Testing"]
act_tools = ["Deployment", "Quality", "Time", "Comms", "TQM", "Standard Work", "Lessons", "Risk Matrix", "Stakeholders", "Change Mgt"]

st.title("CDH Continuous Improvement Toolshed")

st.sidebar.header("Select Tools for Each Phase")
st.sidebar.subheader("Plan")
plan_selection = [
    st.sidebar.selectbox("Select a Plan tool", plan_tools, key="plan1"),
    st.sidebar.selectbox("Select another Plan tool", plan_tools, key="plan2"),
    st.sidebar.selectbox("Select one more Plan tool", plan_tools, key="plan3")
]

st.sidebar.subheader("Do")
do_selection = [
    st.sidebar.selectbox("Select a Do tool", do_tools, key="do1"),
    st.sidebar.selectbox("Select another Do tool", do_tools, key="do2"),
    st.sidebar.selectbox("Select one more Do tool", do_tools, key="do3")
]

st.sidebar.subheader("Check")
check_selection = [
    st.sidebar.selectbox("Select a Check tool", check_tools, key="check1"),
    st.sidebar.selectbox("Select another Check tool", check_tools, key="check2"),
    st.sidebar.selectbox("Select one more Check tool", check_tools, key="check3")
]

st.sidebar.subheader("Act")
act_selection = [
    st.sidebar.selectbox("Select an Act tool", act_tools, key="act1"),
    st.sidebar.selectbox("Select another Act tool", act_tools, key="act2"),
    st.sidebar.selectbox("Select one more Act tool", act_tools, key="act3")
]

st.markdown("## 🔧 Tools Selection")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🟡 Plan Tools")
    for tool in plan_selection:
        st.markdown(f"🛠️ {tool}")

    st.markdown("### 🔵 Do Tools")
    for tool in do_selection:
        st.markdown(f"🛠️ {tool}")

with col2:
    st.markdown("### 🟠 Check Tools")
    for tool in check_selection:
        st.markdown(f"🛠️ {tool}")

    st.markdown("### 🟢 Act Tools")
    for tool in act_selection:
        st.markdown(f"🛠️ {tool}")

st.success("Select the best tools for your Continuous Improvement journey!")
