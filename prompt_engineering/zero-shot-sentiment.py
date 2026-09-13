
from model import load_model, generate_response

# Helper

def run_experiment(title,tokenizer,model,messages,temperature=0.7,top_p=0.95,max_new_tokens=150):
    print(title)

    response = generate_response(tokenizer=tokenizer,model=model,messages=messages,temperature=temperature,top_p=top_p,max_new_tokens=max_new_tokens)
    print("MODEL RESPONSE: ",response)
    print("\n")

# ZERO-SHOT - sentiment classification

def zero_shot_sentiment(tokenizer,model):
    messages = [
        {
            "role" : "system",
            "content": (
                "You are a sentiment classfication system."
                "classify the review as Positive, Negative, Or Neutral."
            )
        },
        {
            "role":"user",
            "content":"""
Review:
"the Laptop looks excellent and the performance is very fast, "
"but the battery life is disappointing"

return only:
Positive
Negative,
or
Neutral
"""
        }
    ]    

    run_experiment("1. ZERO_SHOT- Sentiment Classfication",tokenizer,model,messages,temperature=0.2)
    
def main():
    tokenizer, model = load_model()

    zero_shot_sentiment(tokenizer,model)

if __name__ == "__main__":
    main()
