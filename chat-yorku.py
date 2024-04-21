import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_path = "data/zephyr-7b-sft-lora"
tokenizer = AutoTokenizer.from_pretrained(model_path)
print("Loading AutoModelForCausalLM...")

model = AutoModelForCausalLM.from_pretrained(model_path)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device).half()  # Convert to half precision

def generate_response(question):
    torch.cuda.empty_cache()  # Clear unused memory
    messages = [
        {"role": "system", "content": "You are a friendly chatbot who is an expert in content about York University"},
        {"role": "user", "content": question},
    ]
    input_ids = tokenizer.apply_chat_template(messages, truncation=True, add_generation_prompt=True, return_tensors="pt").to(device)

    with torch.no_grad():
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
