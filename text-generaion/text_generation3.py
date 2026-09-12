import torch
from transformers import AutoTokenizer, AutoModelForCausalLM


MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


def load_model():

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME
    )

    model.eval()

    return tokenizer, model


def generate_response(
    tokenizer,
    model,
    user_prompt
):

    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        },
        {
            "role": "user",
            "content": user_prompt
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        text,
        return_tensors="pt"
    )

    with torch.no_grad():

        output_ids = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )

    new_tokens = output_ids[
        0,
        inputs["input_ids"].shape[-1]:
    ]

    response = tokenizer.decode(
        new_tokens,
        skip_special_tokens=True
    )

    return response


def main():

    tokenizer, model = load_model()

    while True:

        prompt = input("\nYou: ")

        if prompt.lower() == "quit":
            break

        response = generate_response(
            tokenizer,
            model,
            prompt
        )

        print("AI:", response)


if __name__ == "__main__":
    main()