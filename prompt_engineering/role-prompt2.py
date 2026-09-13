
from model import load_model, generate_response

# Helper

def run_experiment(title,tokenizer,model,messages,temperature=0.7,top_p=0.95,max_new_tokens=150):
    print(title)

    response = generate_response(tokenizer=tokenizer,model=model,messages=messages,temperature=temperature,top_p=top_p,max_new_tokens=max_new_tokens)
    print("MODEL RESPONSE: ",response)
    print("\n")


def role_prompt2(tokenizer,model):

    messages = [
        {
            "role":"system",
            "content":"""
You are a senior software engineering interviewer.

Interview the candiate for a java backend developer position.

Ask one question at a time.

Start with a medium-level Java question.

After the candiate answers:
-evaluate the answer
-identify mistakes
-give a score out of 10
-ask the next question
"""
        },
        {
            "role":"user",
            "content":"""
Start the interview.
"""
        }
    ]
    run_experiment("ROLE-PROMPT Interviewer",tokenizer,model,messages,temperature=0.2)
    
def main():
    tokenizer, model = load_model()

    role_prompt2(tokenizer,model)

if __name__ == "__main__":
    main()
