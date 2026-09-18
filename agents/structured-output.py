import ollama
import json

MODEL = "qwen2.5:3b"

messages = [
    {
        "role":"system",
        "content":"""
Classify the user's request.

Return JSON:

{
    "intent":"...",
    "confidence":0.0
}

Possible intents:
refund
technical_support
general_question
"""
    },
    {
        "role":"user",
        "content":"I want my money back."
    }
]

response = ollama.chat(
    model=MODEL,
    messages=messages,
    format="json"
)

data = json.loads(
    response["message"]["content"]
)

print("Intent: ",data["intent"])
print("Confidence: ",data["confidence"])

# Intent:  refund
# Confidence:  0.95