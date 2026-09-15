from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import re

# Load the document
loader = TextLoader(
    os.path.join(os.path.dirname(__file__), "doc", "dream.txt"),
    encoding="utf-8"
)

documents = loader.load()

# Print loaded documents
print(documents)


# Data cleaning function

def clean_text(text):
    # Remove unwanted characters (eg. digits, special characters)

    text = re.sub(r"[^a-zA-Z\s]","",text)

    #normalize whitespace
    text = re.sub(r"\s+"," ",text).strip()

    #convert to lowercase
    text = text.lower()

    return text

document = loader.load()

cleaned_documents = [clean_text(doc.page_content) for doc in document]

print(cleaned_documents)


# splitting the text into characters
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
texts = text_splitter.split_documents(documents)

texts = [clean_text(text.page_content) for text in texts]
print(texts)


