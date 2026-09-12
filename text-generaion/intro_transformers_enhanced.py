
from transformers import pipeline, AutoTokenizer

def create_simple_llm():
    model_name = "distilgpt2"
    generator = pipeline("text-generation",model=model_name,pad_token_id=50256)
    return generator

def generate_text(generator,prompt, max_length=100):

    res = generator(
        prompt,
        max_length=max_length,
        num_return_sequences=1,
        do_sample=True,
        temperature=0.7,
    )
    return res[0]["generated_text"]

def run_llm_demo():
    print("Loading Simple LLM Model...")
    generator = create_simple_llm()

    prompts = [
        "The quick brown fox",
        "Once upon a time",
        "Python programming is",
    ]

    for prompt in prompts:
        print("Prompt: ",prompt)
        print("Generated: ",generate_text(generator,prompt))
        input("Press Enter to see next example..")


def interactive_demo():
    # Allows users to interact with model

    generator = create_simple_llm()
    print("Interactive LLM Demo")
    print("type your prompts (or 'quit' to exit)")

    while True:
        prompt = input("Enter your prompt: ")
        if prompt.lower() == 'quit':
            break

        response = generate_text(generator,prompt)
        print("Generated response: ")
        print(response)


def explain_process():
    # Explains the LLM process with a simple example

    print(" How it works: ")
    print("1. Input text- Tokeniztion - numbers")
    print("2. Numbers - Model processsing - prediction")
    print("Prediction - new token - output text")


    tokenizer = AutoTokenizer.from_pretrained('distilgpt2')
    text = "Hello world"
    tokens = tokenizer.encode(text)
    decoded = tokenizer.decode(tokens)

    print("Example Tokenizations: ")
    print(f"original text: {text}")
    print(f"As tokens (numbers): {tokens}")
    print(f"Decoded back: {decoded}")



if __name__ == "__main__":
    print("Choose  a demo: ")
    print("1. Run basic demonstraction")
    print("2. Interactive Mode")
    print("3. Explain the process")

    choice = input("Enter your choice(1-3): ")

    if choice == '1':
        run_llm_demo()
    elif choice == '2':
        interactive_demo()
    elif choice == '3':
        explain_process()        
