import streamlit as st
import plotly.express as px

from database import initialize_database, get_schema
from agent import agent

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }
    .main-title {
        font-size: 2.7rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        font-size: 1.05rem;
        color: #777;
        margin-bottom: 2rem;
    }
    .metric-card {
        padding: 1.2rem;
        border-radius: 12px;
        border: 1px solid rgba(128, 128, 128, 0.2);
        background: rgba(128, 128, 128, 0.05);
        text-align: center;
    }
    .metric-title {
        font-size: 0.85rem;
        color: #777;
        margin-bottom: 0.3rem;
    }
    .metric-value {
        font-size: 1.7rem;
        font-weight: 700;
    }
    .query-box {
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid rgba(128, 128, 128, 0.25);
        margin-bottom: 1rem;
    }
    .footer {
        text-align: center;
        color: #888;
        font-size: 0.8rem;
        margin-top: 3rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

initialize_database()

if "history" not in st.session_state:
    st.session_state.history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None

with st.sidebar:
    st.header("⚙️ Data Analyst")
    st.caption("Natural language → SQL → Database → Insights")
    st.divider()

    st.subheader("🗄️ Database")
    st.success("SQLite database connected")

    with st.expander("View Database Schema"):
        schema = get_schema()
        st.code(schema, language="text")

    st.divider()

    st.subheader("💬 Example Questions")
    examples = [
        "What are the top 5 products by revenue?",
        "Which city has the most customers?",
        "What is the total revenue?",
        "Show the total quantity sold for each product.",
        "Which product generated the highest revenue?",
        "Show monthly order counts.",
        "What is the average customer age?"
    ]

    for example in examples:
        if st.button(example, key=f"example_{example}", use_container_width=True):
            st.session_state.selected_question = example

    st.divider()

    st.subheader("🤖 Agent")
    st.write("**LLM:** Gemini")
    st.write("**Framework:** LangGraph")
    st.write("**Database:** SQLite")
    st.write("**Visualization:** Plotly")
    st.write("**UI:** Streamlit")

    st.divider()

    st.subheader("🕘 Query History")
    if st.session_state.history:
        for index, item in enumerate(reversed(st.session_state.history)):
            st.caption(f"{len(st.session_state.history) - index}. {item}")
    else:
        st.caption("No queries yet.")

st.markdown('<div class="main-title">📊 AI Data Analyst</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="subtitle">
    Ask questions about your database using natural language.
    The AI agent generates SQL, executes it, repairs SQL errors,
    analyzes the results and creates visualizations.
    </div>
    """,
    unsafe_allow_html=True
)

selected_question = st.session_state.get("selected_question", "")

question = st.text_area(
    "🔎 Ask your data question",
    value=selected_question,
    placeholder="Example: Which product generated the highest revenue?",
    height=100
)

analyze = st.button("🚀 Analyze Data", type="primary", use_container_width=True)

if analyze:
    if not question.strip():
        st.warning("Please enter a question before running the analysis.")
    else:
        st.session_state.selected_question = ""
        with st.status("🤖 AI Agent is working...", expanded=True) as status:
            st.write("🔍 Inspecting database schema...")

            initial_state = {
                "question": question,
                "schema": "",
                "sql_query": "",
                "error": None,
                "dataframe": None,
                "insights": "",
                "attempts": 0
            }

            try:
                st.write("🧠 Generating SQL query...")
                result = agent.invoke(initial_state)

                if result.get("error"):
                    status.update(label="❌ Analysis failed", state="error")
                else:
                    status.update(label="✅ Analysis completed", state="complete")

                st.session_state.last_result = result
                st.session_state.history.append(question)
                st.session_state.history = st.session_state.history[-10:]

            except Exception as error:
                status.update(label="❌ Application error", state="error")
                st.error(f"Something went wrong: {error}")

result = st.session_state.last_result

if result:
    st.divider()
    st.subheader("🔎 Analysis")
    st.info(f"**Question:** {question}")

    dataframe = result.get("dataframe")
    attempts = result.get("attempts", 0)

    if dataframe is not None:
        row_count = len(dataframe)
        column_count = len(dataframe.columns)
    else:
        row_count = 0
        column_count = 0

    metric1, metric2, metric3 = st.columns(3)

    with metric1:
        st.metric("Rows Returned", row_count)

    with metric2:
        st.metric("Columns", column_count)

    with metric3:
        st.metric("SQL Attempts", attempts)

    st.write("")

    with st.expander("🧠 View Generated SQL", expanded=False):
        st.code(result.get("sql_query", ""), language="sql")

    if result.get("error"):
        st.error("The agent could not successfully execute the generated SQL after multiple attempts.")
        with st.expander("View SQL Error"):
            st.code(result["error"])
    else:
        st.subheader("📋 Query Results")

        if dataframe is not None and not dataframe.empty:
            st.dataframe(dataframe, use_container_width=True, hide_index=True)

            csv_data = dataframe.to_csv(index=False)
            st.download_button(
                label="⬇️ Download CSV",
                data=csv_data,
                file_name="query_results.csv",
                mime="text/csv"
            )
        else:
            st.info("The query executed successfully, but returned no rows.")

        st.divider()
        st.subheader("💡 AI Insights")
        insights = result.get("insights", "")

        if insights:
            st.markdown(insights)
        else:
            st.info("No insights were generated.")

        if dataframe is not None and not dataframe.empty and len(dataframe.columns) >= 2:
            st.divider()
            st.subheader("📈 Visualization")
            columns = dataframe.columns.tolist()

            control1, control2 = st.columns(2)

            with control1:
                x_column = st.selectbox("X-axis", columns, index=0)

            numeric_columns = dataframe.select_dtypes(include="number").columns.tolist()

            with control2:
                if numeric_columns:
                    y_column = st.selectbox("Y-axis", numeric_columns, index=0)
                else:
                    y_column = None

            if y_column:
                chart_type = st.selectbox(
                    "Chart Type",
                    ["Bar Chart", "Line Chart", "Scatter Chart"]
                )

                if chart_type == "Bar Chart":
                    figure = px.bar(
                        dataframe,
                        x=x_column,
                        y=y_column,
                        title=f"{y_column} by {x_column}",
                        text_auto=True
                    )
                elif chart_type == "Line Chart":
                    figure = px.line(
                        dataframe,
                        x=x_column,
                        y=y_column,
                        title=f"{y_column} by {x_column}",
                        markers=True
                    )
                else:
                    figure = px.scatter(
                        dataframe,
                        x=x_column,
                        y=y_column,
                        title=f"{y_column} vs {x_column}"
                    )

                st.plotly_chart(figure, use_container_width=True)
            else:
                st.info("No numeric columns available for visualization.")

if not result:
    st.divider()
    st.subheader("✨ Try asking")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**📊 Sales**\n\nWhich product generated the highest revenue?")

    with col2:
        st.markdown("**👥 Customers**\n\nWhich city has the most customers?")

    with col3:
        st.markdown("**📈 Trends**\n\nShow monthly order counts.")

st.markdown(
    """
    <div class="footer">
        AI Data Analyst • LangGraph + Gemini + SQLite + Plotly
    </div>
    """,
    unsafe_allow_html=True
)