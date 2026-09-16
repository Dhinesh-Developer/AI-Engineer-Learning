from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
import os
import re
import pprint

# Load the document
loader = TextLoader(
    os.path.join(os.path.dirname(__file__), "doc", "dream.txt"),
    encoding="utf-8"
)

documents = loader.load()

# Print loaded documents
# print(documents)


# Data cleaning function

def clean_text(text):
    # Remove unwanted characters (eg. digits, special characters)

    text = re.sub(r"[^a-zA-Z\s]","",text)

    #normalize whitespace
    text = re.sub(r"\s+"," ",text).strip()

    #convert to lowercase
    text = text.lower()

    return text

# splitting the text into characters
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = text_splitter.split_documents(documents)

texts = [clean_text(chunk.page_content) for chunk in chunks]

# FAISS expects an Embeddings implementation, not the response from ollama.embed().
embeddings = OllamaEmbeddings(model="embeddinggemma")

# `texts` contains strings, so use from_texts rather than from_documents.
retriever = FAISS.from_texts(texts, embedding=embeddings).as_retriever(search_kwargs={"k":3}) # k=3 means 3 documents

# query
# query = "what did Martin Luther King Jr. dream about?"
query = "give me a summary of the speech in 5 bullet points?"

docs = retriever.invoke(query)

# pprint.pprint(f" => DOCSL {docs}: ")


# Chat with the model and our docs

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_core.output_parsers import StrOutputParser

# create the chat prompt
prompt = ChatPromptTemplate.from_template(
    "Please use the following docs {docs}, and answer the following question {query}"
)

model = ChatOllama(model="qwen2.5:3b")
chain = prompt | model | StrOutputParser()
response = chain.invoke({"docs": docs, "query":query})
print(f"Response: {response}")

# Response: Martin Luther King Jr. dreamt of a future where everyone is judged based on their character rather than the color of their skin. He envisioned a world where people, particularly African Americans, would no longer face racial discrimination. King's dream also encompassed a society where freedom is available to everyone, and where justice and equal opportunities are guaranteed for all, irrespective of their background. He highlighted a vision where former slaves and their descendants could live side by side in brotherhood. Additionally, King emphasized the importance of peaceful resistance against injustice and his message continues to inspire discussions about equality, civil rights, justice, and human dignity, fostering a belief in a better future where different people can live in harmony.

# Response: - The speech is remembered not only for its historical significance but also as a powerful example of leadership courage and hope.
# - It became one of the most important speeches in American history, influencing discussions on equality, civil rights, justice, and human dignity.
# - It emphasizes the equality of all people and the freedom from racial discrimination.
# - King demanded civil and economic rights for African Americans.
# - King envisioned a future where people would be judged by their character rather than by the color of their skin, symbolizing a more inclusive and just society.

# Output
# (" => DOCSL [Document(id='455f6dcf-dd21-4d26-958d-d2715fea2dbb', metadata={}, "
#  "page_content='i have a dream martin luther king jr august martin luther king "
#  'jr delivered his famous i have a dream speech during the march on washington '
#  'for jobs and freedom on august the speech called for an end to racism and '
#  'demanded civil and economic rights for african americans king described his '
#  'vision of a future in which people would be judged by their character rather '
#  "than by the color of their skin'), "
#  "Document(id='389088f3-4415-4085-8b0a-275e8f1a4fea', metadata={}, "
#  "page_content='king spoke about freedom equality justice and hope he "
#  'emphasized that the struggle for civil rights required determination and '
#  'peaceful action he described a dream in which former slaves and the '
#  'descendants of former slave owners could sit together in brotherhood he '
#  "imagined a country where freedom would be available to everyone'), "
#  "Document(id='0f784a9e-2403-4480-bc45-aa9b57acaffc', metadata={}, "
#  "page_content='the speech became one of the most important speeches in "
#  'american history its message continues to influence discussions about '
#  'equality civil rights justice and human dignity the central ideas of the '
#  'speech include equality for all people freedom from racial discrimination '
#  'justice and equal opportunities peaceful resistance against injustice hope '
#  "for a better future brotherhood among people of different backgrounds')]: ")
