import ollama

MODEL = "qwen2.5:3b"

class Agent:
    def __init__(self,model):
        self.model = model
        self.messages = [
            {"role" : "system",
                        "content":"""
            You are a helpful AI assistant.
            Remember the conversation context.
            """}
        ]

    def run(self,user_input):
        self.messages.append({
            "role":"user",
            "content":user_input
        })    

        response = ollama.chat(
            model=self.model,
            messages=self.messages
        )

        assistant_response = response["message"]
        self.messages.append(
            {"role":"assistant","content":assistant_response["content"]}
        )

        return assistant_response["content"]

agent = Agent(MODEL)
print(agent.run("My name is Dhinesh. I from VBM, GENAI developer"))
print(agent.run("What is my name?"))
print(agent.run("i am from ?"))
print(agent.run("which role i am working?"))

# Great to meet Dhinesh! I believe you're from VBM, which is a company known for developing artificial intelligence solutions, and you are the developer of GENAI. Is there something specific you'd like to discuss or work on? Do you have any projects or areas of interest within the GENAI platform that you'd like to discuss or work on?
# Your name is Dhinesh as you introduced yourself earlier in our conversation. Is there something specific you would like to discuss or any particular topic you'd like to explore further?
# You are from VBM, which is the company where you are a developer of GENAI (though I'm not sure of the full name or details of the project without more information). Is there anything specific you would like to discuss or any particular area of interest within your work you'd like to explore?
# Based on your introduction, it sounds like you are working as a developer for GENAI at VBM. If you could provide more details about the specific role or project you are working on, I could offer more tailored information or insights. What is your current role within the GENAI project at VBM?