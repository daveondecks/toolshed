import streamlit as st

# Define tools under each category
plan_tools = ["MoSCoW", "Five Ys", "VSM", "Flow Chart", "Six S’s", "Process Map", "DMAIC", "RACI", "Route Cause", "VOC"]
do_tools = ["Gemba", "Kaizen", "SPC", "Kanban", "Pareto Chart", "Regression", "Poka-yoke", "SIPOC", "FMEA", "Asana"]
check_tools = ["Control Charts", "Check sheet", "Dashboard", "X-Matrix", "Heat Map", "Estimation", "DPMO", "Benchmarking", "Discovery", "Testing"]
act_tools = ["Deployment", "Quality", "Time", "Comms", "TQM", "Standard Work", "Lessons", "Risk Matrix", "Stakeholders", "Change Mgt"]

st.title("CDH Continuous Improvement Toolshed")

# Create the toolbox layout
st.markdown(
    """
    <style>
        .toolbox {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .handle {
            width: 200px;
            height: 50px;
            background: black;
            border-radius: 25px 25px 0 0;
            text-align: center;
            color: white;
            font-weight: bold;
            padding-top: 10px;
        }
        .box {
            width: 250px;
            height: 50px;
            background: yellow;
            margin: 5px;
            border: 1px solid black;
        }
    </style>
    <div class="toolbox">
        <div class="handle">Tools</div>
        <div class="box"></div>
        <div class="box"></div>
        <div class="box"></div>
    </div>
    """,
    unsafe_allow_html=True
)

# Dropdowns at each corner of the slide
st.sidebar.header("Select Tools for Each Phase")
st.sidebar.subheader("Plan")
st.sidebar.selectbox("Select a Plan tool", plan_tools, key="plan1")
st.sidebar.selectbox("Select another Plan tool", plan_tools, key="plan2")
st.sidebar.selectbox("Select one more Plan tool", plan_tools, key="plan3")

st.sidebar.subheader("Do")
st.sidebar.selectbox("Select a Do tool", do_tools, key="do1")
st.sidebar.selectbox("Select another Do tool", do_tools, key="do2")
st.sidebar.selectbox("Select one more Do tool", do_tools, key="do3")

st.sidebar.subheader("Check")
st.sidebar.selectbox("Select a Check tool", check_tools, key="check1")
st.sidebar.selectbox("Select another Check tool", check_tools, key="check2")
st.sidebar.selectbox("Select one more Check tool", check_tools, key="check3")

st.sidebar.subheader("Act")
st.sidebar.selectbox("Select an Act tool", act_tools, key="act1")
st.sidebar.selectbox("Select another Act tool", act_tools, key="act2")
st.sidebar.selectbox("Select one more Act tool", act_tools, key="act3")

st.success("Select the best tools for your Continuous Improvement journey!")
