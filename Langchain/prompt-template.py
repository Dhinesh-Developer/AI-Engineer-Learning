from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

# Initialize Ollama model
model = init_chat_model(
    "qwen2.5:3b",
    model_provider="ollama"
)

# System prompt
system_template = "Translate the following from English into {language}."

# Create prompt template
prompt_template = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("user", "{text}")
])

# Fill the prompt
prompt = prompt_template.invoke({
    "language": "Tamil",
    "text": "Hi, how are you?"
})

print("Prompt:")
print(prompt)

# Invoke the model
response = model.invoke(prompt)

print("\nResponse:")
print(response.content)

# Prompt:
# messages=[SystemMessage(content='Translate the following from English into Tamil.', additional_kwargs={}, response_metadata={}), HumanMessage(content='Hi, how are you?', additional_kwargs={}, response_metadata={})]

# Response:
# வணக்கம், தோற்பார்வை你怎么?