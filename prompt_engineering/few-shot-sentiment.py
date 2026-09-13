
from model import load_model, generate_response

# Helper

def run_experiment(title,tokenizer,model,messages,temperature=0.7,top_p=0.95,max_new_tokens=150):
    print(title)

    response = generate_response(tokenizer=tokenizer,model=model,messages=messages,temperature=temperature,top_p=top_p,max_new_tokens=max_new_tokens)
    print("MODEL RESPONSE: ",response)
    print("\n")


def few_shot_sentiment(tokenizer,model):
    messages = [
        {
            "role":"system",
            "content":(
                "You classify product reviews into Positive, Negative, Or Netural."
            )
        },
        {
            "role":"user",
            "content":"""
Here are examples.

Example 1:
Review: "The phone camera is amazing."
Classfication: Positive

Example 2:
Review: "The phone stopped working after two days."
Classfication: Negative

Now Classify this review:

Review: "The phone preformance is good, but the display is average."

Return only the classfication.

"""
        }
    ]

    run_experiment("1. ZERO_SHOT- Summarization",tokenizer,model,messages,temperature=0.2)
    
def main():
    tokenizer, model = load_model()

    few_shot_sentiment(tokenizer,model)

if __name__ == "__main__":
    main()
