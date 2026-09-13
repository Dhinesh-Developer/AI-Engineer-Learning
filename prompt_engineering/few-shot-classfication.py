
from model import load_model, generate_response

# Helper

def run_experiment(title,tokenizer,model,messages,temperature=0.7,top_p=0.95,max_new_tokens=150):
    print(title)

    response = generate_response(tokenizer=tokenizer,model=model,messages=messages,temperature=temperature,top_p=top_p,max_new_tokens=max_new_tokens)
    print("MODEL RESPONSE: ",response)
    print("\n")


def few_shot_classifcation(tokenizer,model):
    messages = [
        {
            "role":"system",
            "content":(
                "Classify the user's request into one of these intents: LOGIN, PAYMENT, REFUND, or TECHNICAL_SUPPORT"
            )
        },
        {
            "role":"user",
            "content":"""
Examples: 

User: "I cannot remember my password."
Intent: LOGIN

User: "My card was charged twice."
Intent: PAYMENT

User: "I want my money back."
Intent: REFUND

User: "The application keeps crashing."
Intent: TECHNICAL_SUPPORT

Now classify: 
"I paid for the subscription but the transaction failed."

Return only the intent.
"""
        }
    ]

    run_experiment("1. FEW SHOT- classification",tokenizer,model,messages,temperature=0.2)
    
def main():
    tokenizer, model = load_model()

    few_shot_classifcation(tokenizer,model)

if __name__ == "__main__":
    main()
