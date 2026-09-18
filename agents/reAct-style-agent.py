import ollama

MODEL = 'qwen2.5:3b'

def calculator(expression):
    return str(eval(expression))

messages = [
    {
        "role":"system",
            "content":"""
        You are an agent.
        
        When you need a calculation,
        respond with:
        
        ACTION: calculator
        INPUT: mathematical expression
        
        Ortherwise respond with
        FINAL: answer
        
        """
    },
    {
        "role":"user",
        "content":"What is 45 * 20?"
    }
]

while True:
    response = ollama.chat(
        model=MODEL,
        messages=messages
    )

    text = response["message"]["content"]
    print("MODEL: ",text)

    if text.startswith("FINAL:"):
        break

    if "ACTION: calculator" in text:
        expression = text.split(
            "INPUT:"
        )[1].strip()

        result = calculator(expression=expression)

        messages.append(
            {
                "role":"assistant",
                "content":text
            }
        )

        messages.append(
            {
                "role":"user",
                "content":f"OBSERAVTION: {result}"
            }
        )

# MODEL:  ACTION: calculator
# INPUT: 45 * 20
# MODEL:  FINAL: 900
