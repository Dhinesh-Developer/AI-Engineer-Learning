import streamlit as st
from datetime import datetime
from agent import create_research_agent

# PAGE CONFIGURATION


st.set_page_config(
    page_title="Autonomous Web Research Agent",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CUSTOM CSS
st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #777;
        margin-bottom: 25px;
    }

    .research-box {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(128,128,128,0.25);
        margin-bottom: 20px;
    }

    .status-box {
        padding: 15px;
        border-radius: 10px;
        background-color: rgba(128,128,128,0.08);
        margin-top: 10px;
        margin-bottom: 10px;
    }

    .metric-box {
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid rgba(128,128,128,0.25);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# SESSION STATE

if "research_report" not in st.session_state:
    st.session_state.research_report = ""

if "research_topic" not in st.session_state:
    st.session_state.research_topic = ""

if "research_history" not in st.session_state:
    st.session_state.research_history = []


# SIDEBAR

with st.sidebar:
    st.header("⚙️ Research Settings")
    search_limit = st.slider(
        "Maximum searches",
        min_value=1,
        max_value=5,
        value=5
    )
    st.caption(
        "Controls approximately how many web searches "
        "the research agent should perform."
    )

    st.divider()
    st.subheader("💡 Example Topics")
    example_topics = [
        "Latest trends in AI software testing",
        "Future of Generative AI in software development",
        "How AI agents are changing software engineering",
        "Latest advancements in RAG systems",
        "AI applications in cybersecurity"
    ]

    for example in example_topics:
        if st.button(
            example,
            use_container_width=True
        ):
            st.session_state.research_topic = example

    st.divider()
    st.subheader("🤖 Agent Architecture")
    st.markdown(
        """
        **User**
        ↓
        
        **Streamlit UI**
        ↓
        
        **AI Research Agent**
        ↓
        **LLM Reasoning**
        ↓
        **Web Search Tool**
        ↓
        **Tavily**
        ↓
        **Web**
        ↓
        **Research Report**
        """
    )

    st.divider()
    st.caption(
        "Built with Streamlit + LangChain + Groq + Tavily"
    )


# MAIN HEADER

st.markdown(
    '<div class="main-title">🔎 Autonomous Web Research Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
    An AI agent that autonomously searches the web, gathers information,
    reasons over the results, and generates a structured research report.
    </div>
    """,
    unsafe_allow_html=True
)


# HOW IT WORKS

with st.expander("🧠 How does this AI Agent work?"):
    st.markdown(
        """
        ### Agent Workflow

        The agent follows a ReAct-style workflow:

        **1. Understand**
        
        The agent understands the research topic.

        **2. Plan**
        
        It breaks the topic into smaller research questions.

        **3. Search**
        
        It generates search queries and calls the web search tool.

        **4. Observe**
        
        It receives information from the web.

        **5. Reason**
        
        It evaluates whether more information is required.

        **6. Search Again**
        
        If necessary, the agent performs additional searches.

        **7. Synthesize**
        
        The agent combines the collected information.

        **8. Generate Report**
        
        Finally, it produces a structured Markdown research report.

        ### Core Loop

        `Reason → Act → Observe → Reason → Act → Observe → Final`
        """
    )

# RESEARCH INPUT

st.subheader("📝 Research Topic")

topic = st.text_area(
    "What do you want the AI agent to research?",
    value=st.session_state.research_topic,
    placeholder=(
        "Example:\n"
        "Compare the latest trends in AI agents and "
        "their applications in software engineering."
    ),
    height=150
)


# BUTTONS

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    start_research = st.button(
        "🚀 Start Research",
        use_container_width=True,
        type="primary"
    )

with col2:
    clear_report = st.button(
        "🗑️ Clear",
        use_container_width=True
    )


with col3:
    if st.session_state.research_report:
        download_report = st.download_button(
            label="⬇️ Download",
            data=st.session_state.research_report,
            file_name="research_report.md",
            mime="text/markdown",
            use_container_width=True
        )


# CLEAR

if clear_report:

    st.session_state.research_report = ""
    st.session_state.research_topic = ""

    st.rerun()


# START RESEARCH


if start_research:
    if not topic.strip():
        st.warning(
            "⚠️ Please enter a research topic before starting."
        )
    else:
        st.session_state.research_topic = topic

        # Research status
        st.subheader("🔄 Research Progress")
        status_container = st.empty()
        progress_bar = st.progress(0)
        try:

            status_container.info(
                "🧠 Initializing the research agent..."
            )
            progress_bar.progress(10)
            # Create agent
            agent = create_research_agent()
            status_container.info(
                "🔍 Agent is analyzing the research topic..."
            )
            progress_bar.progress(25)

            # ------------------------------------------------
            # Invoke agent
            # ------------------------------------------------

            result = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": topic
                        }
                    ]
                }
            )

            progress_bar.progress(90)

            status_container.info(
                "📝 Synthesizing the final research report..."
            )

            # ------------------------------------------------
            # Get final message
            # ------------------------------------------------

            final_message = result["messages"][-1]

            report = final_message.content

            # Save report
            st.session_state.research_report = report

            # Save history
            st.session_state.research_history.append(
                {
                    "topic": topic,
                    "time": datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                }
            )

            progress_bar.progress(100)

            status_container.success(
                "✅ Research completed successfully!"
            )

        except Exception as e:

            progress_bar.empty()

            status_container.error(
                "❌ Research failed."
            )

            st.exception(e)


# ============================================================
# DISPLAY REPORT
# ============================================================

if st.session_state.research_report:

    st.divider()

    st.subheader("📄 Research Report")

    # --------------------------------------------------------
    # Report statistics
    # --------------------------------------------------------

    report = st.session_state.research_report

    word_count = len(report.split())

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "📄 Report Words",
            word_count
        )

    with col2:
        st.metric(
            "🔎 Search Limit",
            search_limit
        )

    with col3:
        st.metric(
            "🤖 Agent",
            "ReAct"
        )

    st.divider()

    # Display report
    st.markdown(report)


# RESEARCH HISTORY

if st.session_state.research_history:
    st.divider()
    with st.expander("📚 Research History"):
        for index, item in enumerate(
            reversed(st.session_state.research_history),
            start=1
        ):
            st.markdown(
                f"""
                **{index}. {item["topic"]}**

                🕒 {item["time"]}
                """
            )