# PDF RAG

Install the dependencies:

```bash
python3 -m pip install -r rag/01_pdf_rag/requirements.txt
```

Start the app with Streamlit:

```bash
cd rag/01_pdf_rag
python3 -m streamlit run app.py
```

Do not start it with `python3 app.py`. That runs Streamlit in bare mode and
causes the `missing ScriptRunContext` warning.
