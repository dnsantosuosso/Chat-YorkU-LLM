from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

model_path = "data/zephyr-7b-sft-lora"

tokenizer = AutoTokenizer.from_pretrained(model_path)
print("Loading AutoModelForCausalLM...")

peft_model_id = "data/zephyr-7b-sft-lora"
model = AutoModelForCausalLM.from_pretrained(peft_model_id)

# Assuming you don't have a CUDA GPU or you're running this on a machine without CUDA.
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device).half()  # Convert to half precision

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

    input_ids = tokenizer.apply_chat_template(messages, truncation=True, add_generation_prompt=True, return_tensors="pt").to(device)

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
