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
st.session_state.setdefault("do1", do_tools[0])
st.session_state.setdefault("do2", do_tools[1])
st.session_state.setdefault("do3", do_tools[2])
do_selection = [
    st.sidebar.selectbox("Select a Do tool", do_tools, key="do1"),
    st.sidebar.selectbox("Select another Do tool", do_tools, key="do2"),
    st.sidebar.selectbox("Select one more Do tool", do_tools, key="do3")
]

st.sidebar.subheader("Check")
st.session_state.setdefault("check1", check_tools[0])
st.session_state.setdefault("check2", check_tools[1])
st.session_state.setdefault("check3", check_tools[2])
check_selection = [
    st.sidebar.selectbox("Select a Check tool", check_tools, key="check1"),
    st.sidebar.selectbox("Select another Check tool", check_tools, key="check2"),
    st.sidebar.selectbox("Select one more Check tool", check_tools, key="check3")
]

st.sidebar.subheader("Act")
st.session_state.setdefault("act1", act_tools[0])
st.session_state.setdefault("act2", act_tools[1])
st.session_state.setdefault("act3", act_tools[2])
act_selection = [
    st.sidebar.selectbox("Select an Act tool", act_tools, key="act1"),
    st.sidebar.selectbox("Select another Act tool", act_tools, key="act2"),
    st.sidebar.selectbox("Select one more Act tool", act_tools, key="act3")
]

# Display the full Toolshed UI
st.markdown(
    f"""
    <style>
        .container {{
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            align-items: center;
            width: 100%;
        }}
        .column {{
            width: 45%;
            text-align: center;
            margin-bottom: 20px;
        }}
        .toolbox {{
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-top: 10px;
        }}
        .handle {{
            width: 200px;
            height: 50px;
            background: black;
            border-radius: 25px 25px 0 0;
            text-align: center;
            color: white;
            font-weight: bold;
            padding-top: 10px;
        }}
        .box {{
            width: 250px;
            height: 50px;
            background: yellow;
            margin: 5px;
            border: 1px solid black;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }}
    </style>
    <div class="container">
        <div class="column">
            <h2>Plan</h2>
            <div class="toolbox">
                <div class="handle">Tools</div>
                <div class="box">{plan_selection[0]}</div>
                <div class="box">{plan_selection[1]}</div>
                <div class="box">{plan_selection[2]}</div>
            </div>
        </div>
        <div class="column">
            <h2>Do</h2>
            <div class="toolbox">
                <div class="handle">Tools</div>
                <div class="box">{do_selection[0]}</div>
                <div class="box">{do_selection[1]}</div>
                <div class="box">{do_selection[2]}</div>
            </div>
        </div>
        <div class="column">
            <h2>Check</h2>
            <div class="toolbox">
                <div class="handle">Tools</div>
                <div class="box">{check_selection[0]}</div>
                <div class="box">{check_selection[1]}</div>
                <div class="box">{check_selection[2]}</div>
            </div>
        </div>
        <div class="column">
            <h2>Act</h2>
            <div class="toolbox">
                <div class="handle">Tools</div>
                <div class="box">{act_selection[0]}</div>
                <div class="box">{act_selection[1]}</div>
                <div class="box">{act_selection[2]}</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.success("Select the best tools for your Continuous Improvement journey!")