
from model import load_model, generate_response

# Helper

def run_experiment(title,tokenizer,model,messages,temperature=0.7,top_p=0.95,max_new_tokens=150):
    print(title)

    response = generate_response(tokenizer=tokenizer,model=model,messages=messages,temperature=temperature,top_p=top_p,max_new_tokens=max_new_tokens)
    print("MODEL RESPONSE: ",response)
    print("\n")


def role_prompt(tokenizer,model):

    messages = [
        {
            "role":"system",
            "content":"""
You are a senior Java Backend engineer and mentor.
Your job is to teach Java Concepts to a beginner software engineer.

Rules:
- Explain concepts simply.
- Use pratical examples.
- Avoid unnecessary theory.
- Mention common mistakes.
"""
        },
        {
            "role":"user",
            "content":"""
Explain dependency injection in spring boot.

Include:
1. Simple definition
2. Real-world Examples
3. Small java example
4. Common beginner mistake
"""
        }
    ]
    
    run_experiment("ROLE-PROMPT java mentor",tokenizer,model,messages,temperature=0.2)
    
def main():
    tokenizer, model = load_model()

    role_prompt(tokenizer,model)

if __name__ == "__main__":
    main()
