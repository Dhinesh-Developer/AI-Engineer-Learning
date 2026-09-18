import ollama

MODEL = "qwen2.5:3b"

class Agent:
    def __init__(self,model):
        self.model = model

    def run(self, user_input):
        messages = [
            {"role" : "system",
            "content":"You are a helpful AI agent. Answer the user's question clearly."},
            {
                "role":"user",
                "content":user_input
            }
        ]

        response = ollama.chat(
            model=self.model,
            messages=messages
        )        

        return response["message"]["content"]

agent = Agent(MODEL)
response = agent.run("Explain what an AI agent is in simple terms.")
print(response)    

# An AI agent is like a helper that uses computers to learn from and interact with the world.
#  It's designed to perform tasks or solve problems by itself, often without human intervention. 
# Think of it as a smart robot or computer program that can understand instructions, '
# 'make decisions based on that understanding, and take actions to achieve goals,
#  all with the goal of making people's lives easier or more efficient.