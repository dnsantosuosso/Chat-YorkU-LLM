from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_path = "data/zephyr-7b-sft-lora"

tokenizer = AutoTokenizer.from_pretrained(model_path)
print("Loading AutoModelForCausalLM...")

peft_model_id = "data/zephyr-7b-sft-lora"
# Load the model with automatic device mapping and 4-bit precision
model = AutoModelForCausalLM.from_pretrained(peft_model_id, load_in_4bit=True, device_map="auto")

print("Model is ready for inference.")

def generate_response(question):
    # Disable gradient calculation
    torch.set_grad_enabled(False)
    
    messages = [
        {
            "role": "system",
            "content": "You are a friendly chatbot who is an expert in content about York University",
        },
        {"role": "user", "content": question},
    ]

    # Since the model is already on the correct device, use it directly
    input_ids = tokenizer.apply_chat_template(messages, truncation=True, add_generation_prompt=True, return_tensors="pt")

    outputs = model.generate(
        input_ids=input_ids,
        max_new_tokens=2000,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

if __name__ == '__main__':
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break
        print("Bot:", generate_response(user_input))
