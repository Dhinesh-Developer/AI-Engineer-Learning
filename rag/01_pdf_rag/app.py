import streamlit as st

from rag import (
    add_pdf,
    retrieve,
    generate_answer
)


st.set_page_config(
    page_title="PDF RAG",
    page_icon="📄"
)


st.title("📄 PDF RAG Assistant")

st.write(
    "Upload a PDF and ask questions about it."
)


# -----------------------------
# PDF UPLOAD
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)


if uploaded_file:

    if st.button("Process PDF"):

        with st.spinner(
            "Processing PDF..."
        ):

            chunks = add_pdf(
                uploaded_file
            )

        st.success(
            f"PDF processed successfully. "
            f"{chunks} chunks stored."
        )


# -----------------------------
# QUESTION
# -----------------------------

question = st.text_input(
    "Ask a question"
)


if question:

    with st.spinner(
        "Searching knowledge base..."
    ):

        result = retrieve(
            question
        )

    answer = generate_answer(
        question,
        result["documents"]
    )

    st.subheader("Answer")

    st.write(answer)


    # -------------------------
    # RETRIEVED CONTEXT
    # -------------------------

    with st.expander(
        "🔍 Retrieved Documents"
    ):

        for idx, document in enumerate(
            result["documents"]
        ):

            st.write(
                f"### Result {idx + 1}"
            )

            st.write(document)

            st.write(
                f"Distance: "
                f"{result['distances'][idx]}"
            )

            st.divider()