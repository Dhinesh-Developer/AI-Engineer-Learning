from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)


MODELS = {

    "1": "distilgpt2",

    "2": "gpt2",

    "3": "Qwen/Qwen2.5-0.5B-Instruct"
}


def load_model(model_name):

    print(f"\nLoading: {model_name}")

    tokenizer = AutoTokenizer.from_pretrained(
        model_name
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_name
    )

    model.eval()

    return tokenizer, model


def generate(
    tokenizer,
    model,
    prompt
):

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    output_ids = model.generate(
        **inputs,
        max_new_tokens=80,
        do_sample=True,
        temperature=0.7,
        top_p=0.9
    )

    new_tokens = output_ids[
        0,
        inputs["input_ids"].shape[-1]:
    ]

    return tokenizer.decode(
        new_tokens,
        skip_special_tokens=True
    )


def main():

    print("Available Models")

    for key, model in MODELS.items():
        print(f"{key}. {model}")

    choice = input("\nChoose model: ")

    if choice not in MODELS:
        print("Invalid choice")
        return

    model_name = MODELS[choice]

    tokenizer, model = load_model(
        model_name
    )

    print("\nModel ready.")
    print("Type 'quit' to exit.")

    while True:

        prompt = input("\nYou: ")

        if prompt.lower() == "quit":
            break

        response = generate(
            tokenizer,
            model,
            prompt
        )

        print("\nAI:", response)


if __name__ == "__main__":
    main()