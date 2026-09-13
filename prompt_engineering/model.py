from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


def load_model():

    print("Loading model...")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        dtype="auto",
        device_map="auto"
    )

    print("Model loaded successfully.")

    return tokenizer, model


def generate_response(
    tokenizer,
    model,
    messages,
    max_new_tokens=150,
    temperature=0.7,
    top_p=0.95
):

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    ).to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=max_new_tokens,
        do_sample=True,
        temperature=temperature,
        top_p=top_p
    )

    generated_tokens = outputs[0][inputs["input_ids"].shape[-1]:]

    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    return response.strip()