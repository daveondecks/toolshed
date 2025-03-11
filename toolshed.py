import streamlit as st

# Define tools under each category
plan_tools = ["MoSCoW", "Five Ys", "VSM", "Flow Chart", "Six S’s", "Process Map", "DMAIC", "RACI", "Route Cause", "VOC"]
do_tools = ["Gemba", "Kaizen", "SPC", "Kanban", "Pareto Chart", "Regression", "Poka-yoke", "SIPOC", "FMEA", "Asana"]
check_tools = ["Control Charts", "Check sheet", "Dashboard", "X-Matrix", "Heat Map", "Estimation", "DPMO", "Benchmarking", "Discovery", "Testing"]
act_tools = ["Deployment", "Quality", "Time", "Comms", "TQM", "Standard Work", "Lessons", "Risk Matrix", "Stakeholders", "Change Mgt"]

st.title("CDH Continuous Improvement Toolshed")

# Sidebar Dropdowns
st.sidebar.header("Select Tools for Each Phase")
st.sidebar.subheader("Plan")
st.session_state.setdefault("plan1", plan_tools[0])
st.session_state.setdefault("plan2", plan_tools[1])
st.session_state.setdefault("plan3", plan_tools[2])
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

# PDCA Cycle Explanation
st.markdown("## 🔄 PDCA Continuous Improvement Cycle")

st.markdown("### 🟡 PLAN")
st.markdown("**Identify the issue:** Define the problem, gather relevant data. Formulate a hypothesis. What exactly are you trying to achieve by when? What resources do you need?")

st.markdown("### 🔵 DO")
st.markdown("**Quickly try out a solution:** Implement your plan, but start small. This stage is a controlled experiment, not full-scale deployment. Effective communication at this stage is key.")

st.markdown("### 🟠 CHECK")
st.markdown("**See if it works:** Step back and examine what happened. Did you get the desired result? Why or Why not? Compare your actual outcomes against your predictions. Look for insights, opportunities, costs, lessons, or unexpected consequences.")

st.markdown("### 🟢 ACT")
st.markdown("**Launch or adjust:** If your solution proved effective, how can you implement it more widely? If it fell short, what adjustments are needed? Perhaps you need to return to the planning stage with new insights.")
