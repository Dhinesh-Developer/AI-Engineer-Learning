import os
import tempfile

import streamlit as st

from rag import (
    load_pdf,
    split_documents,
    create_vector_store,
    create_retriever,
    ask_question
)


# ============================================================
# STREAMLIT CONFIG
# ============================================================

st.set_page_config(
    page_title="PDF RAG Assistant",
    page_icon="📚",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("📚 PDF RAG Assistant")

st.write(
    "Ask questions about your PDF using "
    "Qwen 2.5 + EmbeddingGemma + ChromaDB"
)


# ============================================================
# SESSION STATE
# ============================================================

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False

if "pdf_name" not in st.session_state:
    st.session_state.pdf_name = None


# ============================================================
# PDF UPLOAD
# ============================================================

uploaded_file = st.file_uploader(
    "📄 Upload PDF",
    type=["pdf"]
)


# ============================================================
# PROCESS PDF
# ============================================================

if uploaded_file is not None:

    st.info(
        f"Selected PDF: **{uploaded_file.name}**"
    )

    if st.button(
        "🚀 Process PDF",
        type="primary"
    ):

        temp_path = None

        try:

            # ------------------------------------------------
            # SAVE UPLOADED PDF
            # ------------------------------------------------

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ) as temp_file:

                temp_file.write(
                    uploaded_file.getvalue()
                )

                temp_path = temp_file.name


            # ------------------------------------------------
            # CHECK FILE
            # ------------------------------------------------

            file_size = os.path.getsize(
                temp_path
            )

            if file_size == 0:

                st.error(
                    "❌ The uploaded PDF is empty."
                )

                st.stop()


            st.info(
                f"PDF size: "
                f"{file_size / 1024:.2f} KB"
            )


            # ------------------------------------------------
            # LOAD PDF
            # ------------------------------------------------

            with st.spinner(
                "📖 Reading PDF..."
            ):

                documents = load_pdf(
                    temp_path
                )


            if not documents:

                st.error(
                    "❌ No readable pages found in the PDF."
                )

                st.stop()


            st.success(
                f"✅ Loaded {len(documents)} pages"
            )


            # ------------------------------------------------
            # SPLIT DOCUMENT
            # ------------------------------------------------

            with st.spinner(
                "✂️ Splitting PDF into chunks..."
            ):

                chunks = split_documents(
                    documents
                )


            if not chunks:

                st.error(
                    "❌ Could not create chunks from PDF."
                )

                st.stop()


            st.success(
                f"✅ Created {len(chunks)} chunks"
            )


            # ------------------------------------------------
            # CREATE VECTOR STORE
            # ------------------------------------------------

            with st.spinner(
                "🧠 Creating embeddings with "
                "EmbeddingGemma..."
            ):

                vectorstore = create_vector_store(
                    chunks
                )


            st.success(
                "✅ ChromaDB created successfully"
            )


            # ------------------------------------------------
            # CREATE RETRIEVER
            # ------------------------------------------------

            retriever = create_retriever(
                vectorstore
            )


            # ------------------------------------------------
            # SAVE TO SESSION
            # ------------------------------------------------

            st.session_state.retriever = retriever

            st.session_state.pdf_processed = True

            st.session_state.pdf_name = (
                uploaded_file.name
            )


            st.success(
                "🎉 PDF processed successfully!"
            )


        except Exception as error:

            st.error(
                "❌ Failed to process the PDF."
            )

            st.exception(
                error
            )

            # Reset retriever if processing fails
            st.session_state.retriever = None
            st.session_state.pdf_processed = False


        finally:

            # ------------------------------------------------
            # DELETE TEMPORARY FILE
            # ------------------------------------------------

            if temp_path is not None:

                try:

                    if os.path.exists(temp_path):

                        os.unlink(temp_path)

                except Exception:

                    pass


# ============================================================
# PDF STATUS
# ============================================================

if st.session_state.pdf_processed:

    st.success(
        f"📚 Active document: "
        f"{st.session_state.pdf_name}"
    )


# ============================================================
# QUESTION SECTION
# ============================================================

st.divider()

st.subheader(
    "💬 Ask Questions"
)

question = st.text_input(
    "Ask a question about your PDF",
    placeholder="Example: What is the main topic of this document?"
)


# ============================================================
# ANSWER QUESTION
# ============================================================

if question:

    retriever = st.session_state.retriever


    if retriever is None:

        st.warning(
            "⚠️ Please upload and process a PDF first."
        )


    else:

        try:

            with st.spinner(
                "🔍 Searching document..."
            ):

                answer, documents = ask_question(
                    retriever,
                    question
                )


            # ------------------------------------------------
            # ANSWER
            # ------------------------------------------------

            st.subheader(
                "🤖 Answer"
            )

            st.write(
                answer
            )


            # ------------------------------------------------
            # SOURCES
            # ------------------------------------------------

            st.subheader(
                "📚 Sources"
            )


            if documents:

                for index, document in enumerate(
                    documents
                ):

                    page = document.metadata.get(
                        "page",
                        "Unknown"
                    )

                    # PyMuPDF/PyPDF usually use zero-based page
                    # numbers, so display human-friendly page number.
                    if isinstance(page, int):

                        display_page = page + 1

                    else:

                        display_page = page


                    with st.expander(
                        f"Result {index + 1} — "
                        f"Page {display_page}"
                    ):

                        st.write(
                            document.page_content
                        )

            else:

                st.info(
                    "No relevant document chunks found."
                )


        except Exception as error:

            st.error(
                "❌ Error while generating the answer."
            )

            st.exception(
                error
            )