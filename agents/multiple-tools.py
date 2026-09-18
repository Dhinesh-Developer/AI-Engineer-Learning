import ollama

MODEL = "qwen2.5:3b"

def calculator(expression):
    try:
        res = eval(expression)
        return str(res)
    except Exception as err:
        return f"Error: {err}"

tools = [
    {
        "type":"function",
        "function":{
            "name":"calculator",
            "description":"Calculate a mathematical expression.",
            "parameters":{
                "type":"object",
                "properties":{
                    "expression":{
                        "type":"string",
                    }
                },
                "required":["expression"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"get_date",
            "description":"Get today's date.",
            "parameters":{
                "type":"object",
                "properties":{}
            }
        }
    }
]    

messages = [
    {
        "role":"system",
        "content":"You are an AI assistant that can use tools."
    },
    {
        "role":"user",
        "content": "what is today's date and what is 100 + 100"
    }
]

response = ollama.chat(
    model=MODEL,
    messages=messages,
    tools=tools
)

print(response)

# model='qwen2.5:3b' created_at='2026-09-18T01:35:52.212647899Z' done=True done_reason='stop' total_duration=1863293070 load_duration=801065 prompt_eval_count=182 prompt_eval_duration=56995000 eval_count=124 eval_duration=1788525000 message=Message(role='assistant', content='', thinking=None, images=None, tool_name=None, tool_calls=[ToolCall(function=Function(name='get_date', arguments={})), ToolCall(function=Function(name='calculator', arguments={'expression': '100 + 100'})), ToolCall(function=Function(name='get_date', arguments={})), ToolCall(function=Function(name='calculator', arguments={'expression': '100 + 100'})), ToolCall(function=Function(name='get_date', arguments={})), ToolCall(function=Function(name='calculator', arguments={'date': '2023-09-28', 'calculator_result': 200}))]) logprobs=None
