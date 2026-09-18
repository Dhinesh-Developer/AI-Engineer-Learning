
import ollama

llm_name = "llama3.2"


# response = ollama.chat(
#     model=llm_name,
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "Who is Nelson Mandela?"}
#     ]
# )

# print(response["message"]["content"])


# create our own agent

class Agent:

    def __init__(self, system="You are a helpful assistant."):

        self.system = system
        self.messages = []

        if system:
            self.messages.append({
                "role": "system",
                "content": system
            })

    def __call__(self, message):

        self.messages.append({
            "role": "user",
            "content": message
        })

        result = self.execute()

        self.messages.append({
            "role": "assistant",
            "content": result
        })

        return result

    def execute(self):

        response = ollama.chat(
            model=llm_name,
            messages=self.messages,
            options={
                "temperature": 0.0
            }
        )

        return response["message"]["content"]


prompt = """
You are an AI agent that works in a loop of:

Thought
Action
PAUSE
Observation

You have access to tools.

Your available actions are:

1. calculate
Example:
Action: calculate: 4 * 7 / 3

2. planet_mass
Example:
Action: planet_mass: Earth

When you need a tool, output:

Action: tool_name: argument
PAUSE

The program will execute the action and return an Observation.

After receiving the Observation, continue reasoning.

When you have enough information, output:

Answer: your final answer

Example:

Question: What is the combined mass of Earth and Mars?

Thought: I should find the mass of Earth.

Action: planet_mass: Earth
PAUSE

Observation: Earth has a mass of 5.972 * 10^24 kg

Thought: Now I need the mass of Mars.

Action: planet_mass: Mars
PAUSE

Observation: Mars has a mass of 0.64171 * 10^24 kg

Thought: I can now calculate the combined mass.

Action: calculate: 5.972 + 0.64171
PAUSE

Observation: 6.61371

Answer: The combined mass of Earth and Mars is
6.61371 * 10^24 kg.
""".strip()


def calculate(what):
    return eval(what)


def planet_mass(name):

    masses = {
        "Mercury": 0.33011,
        "Venus": 4.8675,
        "Earth": 5.972,
        "Mars": 0.64171,
        "Jupiter": 1898.19,
        "Saturn": 568.34,
        "Uranus": 86.813,
        "Neptune": 102.413
    }

    return f"{name} has a mass of {masses[name]} * 10^24 kg"


known_actions = {
    "calculate": calculate,
    "planet_mass": planet_mass
}


# create the agent

agent = Agent(system=prompt)

# response = agent("What is the mass of the Earth?")
# print(response)
# response = planet_mass("Earth")
# print(response)


# next_response = f"Obseravtion: {response}"
# print(next_response)

# response = agent(next_response)
# print(response)

# # all messages
# print(agent.messages)


# ---------- Complex Query ---------------
# question = "what is the combined mass of Earth and Saturn?"
# response = agent(question)

# print(response)


