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
                        "description":"Mathematical expression such as 25*48"
                    }
                },
                "required":["expression"]
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
        "content": "Calculate 25 * 48."
    }
]

response = ollama.chat(
    model=MODEL,
    messages=messages,
    tools=tools
)

print(response)
