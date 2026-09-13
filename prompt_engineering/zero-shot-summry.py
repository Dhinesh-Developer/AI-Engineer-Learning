
from model import load_model, generate_response

# Helper

def run_experiment(title,tokenizer,model,messages,temperature=0.7,top_p=0.95,max_new_tokens=150):
    print(title)

    response = generate_response(tokenizer=tokenizer,model=model,messages=messages,temperature=temperature,top_p=top_p,max_new_tokens=max_new_tokens)
    print("MODEL RESPONSE: ",response)
    print("\n")

# ZERO-SHOT - sentiment classification

def zero_shot_summary(tokenizer,model):
    messages = [
        {
            "role":"system",
            "content":(
                "You are a professional summarization assistant."
            )
        },
        {
            "role":"user",
            "content":"""
Summarize the following paragraph in exaclty 3 bullet points.

Artificial intelligence is changing software development.
Developers are increasingly using AI assistants for code generation,
debugging, testing, documentation, and code review. However,
developers still need strong programming fundamentals because
AI-generated code can contain bugs, security problems, and incorrect
assumptions. The most effective developers use AI as a productivity
tool while maintaining responsibility for the final software.

return only the 3 bullet points.
"""
        }
    ]  

    run_experiment("1. ZERO_SHOT- Summarization",tokenizer,model,messages,temperature=0.2)
    
def main():
    tokenizer, model = load_model()

    zero_shot_summary(tokenizer,model)

if __name__ == "__main__":
    main()
