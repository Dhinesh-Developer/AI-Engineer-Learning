from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path

# load your document (assuming a text file for thid example)
document_path = Path(__file__).parent / "doc" / "dream.txt"
text_loader = TextLoader(str(document_path), encoding="utf-8")
documents = text_loader.load()

# text splitters
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 20,
    length_function=len,
)

# split the documents
splits = text_splitter.split_documents(documents)
# output the results

for i, split in enumerate(splits):
    print(f"Split {i+1}:\n{split}\n")

# res
    
# Split 1:
# page_content='I Have a Dream

# Martin Luther King Jr.
# August 28, 1963' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 2:
# page_content='Martin Luther King Jr. delivered his famous "I Have a Dream" speech' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 3:
# page_content='during the March on Washington for Jobs and Freedom on August 28, 1963.' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 4:
# page_content='The speech called for an end to racism and demanded civil and economic' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 5:
# page_content='rights for African Americans. King described his vision of a future in' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 6:
# page_content='which people would be judged by their character rather than by the color
# of their skin.' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 7:
# page_content='King spoke about freedom, equality, justice, and hope. He emphasized that' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 8:
# page_content='the struggle for civil rights required determination and peaceful action.' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 9:
# page_content='He described a dream in which former slaves and the descendants of former' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 10:
# page_content='slave owners could sit together in brotherhood. He imagined a country where' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 11:
# page_content='freedom would be available to everyone.' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 12:
# page_content='The speech became one of the most important speeches in American history.' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 13:
# page_content='Its message continues to influence discussions about equality, civil rights,' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 14:
# page_content='justice, and human dignity.' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 15:
# page_content='The central ideas of the speech include:' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 16:
# page_content='1. Equality for all people.
# 2. Freedom from racial discrimination.' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 17:
# page_content='3. Justice and equal opportunities.
# 4. Peaceful resistance against injustice.' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 18:
# page_content='5. Hope for a better future.
# 6. Brotherhood among people of different backgrounds.' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 19:
# page_content='The speech demonstrates how powerful communication can inspire people and' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 20:
# page_content='influence social change. It is remembered not only as a historical speech' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}

# Split 21:
# page_content='but also as a powerful example of leadership, courage, and hope.' metadata={'source': '/home/dhinesh/Ai-engineer/Langchain/doc/dream.txt'}



