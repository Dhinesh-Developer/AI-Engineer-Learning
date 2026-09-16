import streamlit as st

from chain import ask_ai


st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖"
)


st.title("🤖 LangChain AI Assistant")

st.write(
    "Simple AI Assistant using LangChain + Ollama + Qwen"
)


question = st.text_input(
    "Ask something",
    placeholder="What is an API?"
)


if st.button("Ask AI"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Qwen is thinking..."):

            answer = ask_ai(question)

        st.subheader("Answer")

        st.write(answer)