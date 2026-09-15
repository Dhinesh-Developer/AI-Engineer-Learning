import ollama
from langchain.chat_models import init_chat_model

model = init_chat_model("qwen2.5:3b",model_provider="ollama")
response = model.invoke("Hello, how are you?")
print(response)

# content="Hello! I'm an artificial intelligence, so I don't have feelings or a physical presence, but I'm here and ready to assist you. How can I help you today?" additional_kwargs={} response_metadata={'model': 'qwen2.5:3b', 'created_at': '2026-09-15T13:13:21.127631936Z', 'done': True, 'done_reason': 'stop', 'total_duration': 6413160275, 'load_duration': 4264236066, 'prompt_eval_count': 35, 'prompt_eval_duration': 895005000, 'eval_count': 37, 'eval_duration': 1250250000, 'logprobs': None, 'model_name': 'qwen2.5:3b', 'model_provider': 'ollama'} id='lc_run--01a0a533-40d8-7fc1-b572-e17f50180d97-0' tool_calls=[] invalid_tool_calls=[] usage_metadata={'input_tokens': 35, 'output_tokens': 37, 'total_tokens': 72}