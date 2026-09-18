import ollama
import json
import os


MODEL = "qwen2.5:3b"

MEMORY_FILE = "memory.json"


def load_memory():

    if os.path.exists(MEMORY_FILE):

        with open(MEMORY_FILE, "r") as file:

            return json.load(file)

    return []


def save_memory(memory):

    with open(MEMORY_FILE, "w") as file:

        json.dump(
            memory,
            file,
            indent=2
        )


memory = load_memory()


user_input = input("Tell the agent something: ")


memory.append(
    {
        "user": user_input
    }
)


save_memory(memory)


prompt = f"""
Here is the user's previous memory:

{memory}

Respond naturally to the user.
"""


response = ollama.chat(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)


print(
    response["message"]["content"]
)