import ollama

MODEL = "qwen2.5:3b"

messages = [
    {
        "role":"system",
        "content":"You are a helpful assistant."
    }
]

while True:

    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    messages.append(
        {
            "role":"user",
            "content":user_input
        }
    )

    response = ollama.chat(
        model=MODEL,
        messages=messages
    )

    answer = response["message"]["content"]

    messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )

    print("Agent: ",answer)


