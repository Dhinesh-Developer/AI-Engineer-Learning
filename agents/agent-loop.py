
import ollama


MODEL = "llama3.2"

def calculator(expression):
    try:
        return str(eval(expression))
    except Exception as err:
        return f"Error {err}"

def execute_tool(tool_call):
    name = tool_call.function.name
    arguments = tool_call.function.arguments
    if name == "calculator":
        return calculator(arguments["expression"])
    return "Unknown tool"

tools = [
    {
        "type":"function",
        "function":{
            "name":"calculator",
            "description":"Calculate mathematical expressions.",
            "parameters":{
                "type":"object",
                "properties":{
                    "expression":{
                        "type":"string"
                    }
                },
                "required":["expression"]
            }
        }
    }
]

messages = [
    {"role":"system",
     "content":"Use tools when necessary."},
     {"role":"user",
      "content":"Calculate 123 * 45."}
]

while True:

    response = ollama.chat(
        model=MODEL,
        messages=messages,
        tools=tools
    )  

    message = response["message"]
    messages.append(message) 

    if not message.get("tool_calls"):
        print(message["content"])
        break

    for tool_call in message["tool_calls"]:
        res = execute_tool(tool_call=tool_call)
        messages.append(
            {"role":"tool",
            "content":res}
        )

# The result of the calculation 123 * 45 is 5535.
