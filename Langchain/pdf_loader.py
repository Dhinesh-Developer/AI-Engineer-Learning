from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader

document_path = Path(__file__).parent / "doc" / "HLD.pdf"

document_loader = TextLoader(str(document_path), encoding="utf-8")

docs = document_loader.load()
print("PDF Documents: ",docs)
