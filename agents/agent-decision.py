import ollama
import json

MODEL = "qwen2.5:3b"

messages = [
    {
        "role": "system",
        "content": """
You are an AI agent planner.

Return JSON:

{
    "action": "calculator | final",
    "input": "...",
    "reason": "short explanation"
}
"""
    },
    {
        "role": "user",
        "content":
        "Calculate 250 * 4."
    }
]


response = ollama.chat(
    model=MODEL,
    messages=messages,
    format="json"
)

decision = json.loads(
    response["message"]["content"]
)

print("Action:",decision["action"])
print("Input:",decision["input"])
print("Reason:",decision["reason"])

# Action: calculator | final
# Input: 250 * 4
# Reason: Perform multiplication operation
