from transformers import pipeline


def create_generator():
    model_name = "distilgpt2"

    generator = pipeline(
        "text-generation",
        model=model_name,
        device=-1
    )

    return generator


def generate_text(generator, prompt):
    result = generator(
        prompt,
        max_new_tokens=50,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
        num_return_sequences=1
    )

    return result[0]["generated_text"]


def main():

    generator = create_generator()

    prompts = [
        "Artificial intelligence is",
        "Python programming is",
        "The future of software engineering is"
    ]

    for prompt in prompts:

        print("\nPrompt:", prompt)

        response = generate_text(
            generator,
            prompt
        )

        print("Response:", response)


if __name__ == "__main__":
    main()