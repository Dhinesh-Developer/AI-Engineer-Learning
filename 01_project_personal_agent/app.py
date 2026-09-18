
import streamlit as st
from agent import PersonalAgent
from database import initialize_database


# PAGE CONFIGURATION

st.set_page_config(
    page_title="Local Personal AI Agent",
    page_icon="🤖",
    layout="wide"
)

# INITIALIZE DATABASE

initialize_database()


# SESSION STATE

if "agent" not in st.session_state:
    st.session_state.agent = PersonalAgent()

if "messages" not in st.session_state:
    st.session_state.messages = []


# SIDEBAR
with st.sidebar:

    st.title("🤖 Personal AI Agent")
    st.write(
        "Local AI agent powered by Ollama."
    )
    st.divider()

    st.subheader("Available Tools")

    st.write("🧮 Calculator")
    st.write("📝 Save Notes")
    st.write("📚 List Notes")
    st.write("🔎 Search Notes")
    st.write("🕒 Current Time")

    st.divider()

    if st.button(
        "🔄 Reset Conversation",
        use_container_width=True
    ):
        st.session_state.agent.reset()
        st.session_state.messages = []
        st.rerun()



# MAIN HEADER

st.title("🤖 Local Personal AI Agent")
st.caption(
    "Python + Ollama + SQLite + Streamlit"
)


# DISPLAY PREVIOUS MESSAGES

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# CHAT INPUT

user_input = st.chat_input(
    "Ask your local AI agent..."
)

if user_input:
    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # Run agent
    with st.chat_message("assistant"):
        with st.spinner(
            "Agent is thinking..."
        ):

            answer, trace = (
                st.session_state.agent.run(
                    user_input
                )
            )

        st.markdown(answer)

        # Show tool execution details
        if trace:

            with st.expander(
                "🔧 Agent Tool Execution"
            ):

                for item in trace:
                    st.write(
                        f"**Step {item['step']}**"
                    )

                    st.write(
                        f"Tool: `{item['tool']}`"
                    )

                    st.write(
                        "Arguments:"
                    )

                    st.json(
                        item["arguments"]
                    )

                    st.write(
                        "Result:"
                    )

                    st.json(
                        item["result"]
                    )
                    st.divider()

    # Save assistant response
   
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )