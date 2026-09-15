import streamlit as st

from rag import (
    add_document,
    retrieve,
    generate_answer
)


st.set_page_config(
    page_title="Notes RAG",
    page_icon="🎓"
)


st.title(
    "🎓 Course Notes RAG Assistant"
)


uploaded_files = st.file_uploader(
    "Upload your course PDFs",
    type=["pdf"],
    accept_multiple_files=True
)


if uploaded_files:

    if st.button(
        "Process Documents"
    ):

        total_chunks = 0

        with st.spinner(
            "Processing documents..."
        ):

            for pdf in uploaded_files:

                count = add_document(
                    pdf,
                    pdf.name
                )

                total_chunks += count


        st.success(
            f"Processed "
            f"{len(uploaded_files)} documents "
            f"and {total_chunks} chunks."
        )


question = st.text_input(
    "Ask something from your notes"
)


if question:

    with st.spinner(
        "Searching notes..."
    ):

        results = retrieve(
            question
        )


    answer = generate_answer(
        question,
        results
    )


    st.subheader("Answer")

    st.write(answer)


    with st.expander(
        "📚 Sources"
    ):

        documents = results[
            "documents"
        ][0]

        metadatas = results[
            "metadatas"
        ][0]

        distances = results[
            "distances"
        ][0]


        for i in range(
            len(documents)
        ):

            st.write(
                f"### Result {i + 1}"
            )

            st.write(
                f"**Source:** "
                f"{metadatas[i]['source']}"
            )

            st.write(
                f"**Page:** "
                f"{metadatas[i]['page']}"
            )

            st.write(
                f"**Distance:** "
                f"{distances[i]:.4f}"
            )

            st.write(
                documents[i]
            )

            st.divider()