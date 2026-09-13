
from model import load_model, generate_response

# Helper

def run_experiment(title,tokenizer,model,messages,temperature=0.7,top_p=0.95,max_new_tokens=500):
    print(title)

    response = generate_response(tokenizer=tokenizer,model=model,messages=messages,temperature=temperature,top_p=top_p,max_new_tokens=max_new_tokens)
    print("MODEL RESPONSE: ",response)
    print("\n")


def reasoning(tokenizer,model):

    messages = [
        {
            "role":"system",
            "content":"""
You are a careful problem-solving assistant.

Solve the problems systematically.

Give: 

1.Approach
2.Key calculation or reasoning.
3.Final answer.

Keep the messages concise.
"""
        },{
            "role":"user",
            "content":"""
A company has 120 employees.

60 know java.
50 know python.
20 know both Java and python.

How many employees know at least one of two languages?

Explain the solution breifly.
"""
        }
    ]
    run_experiment("ROLE-PROMPT Interviewer",tokenizer,model,messages,temperature=0.7)
    
def main():
    tokenizer, model = load_model()

    reasoning(tokenizer,model)

if __name__ == "__main__":
    main()
