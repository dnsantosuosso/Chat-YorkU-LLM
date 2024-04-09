from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
import torch

app = Flask(__name__)

model_path = "/Users/diegosantosuosso/Desktop/Chat-YorkU/data/zephyr-7b-sft-lora"

tokenizer = AutoTokenizer.from_pretrained(model_path)
print("Running AutoModelForCausalLM...")
model = AutoModelForCausalLM.from_pretrained(model_path)

@app.route('/Answer', methods=['POST'])
def answer():
    data = request.get_json(force=True)  # Get data from POST request

    # Extract the question from the POST data
    question = data.get('question', '')

    # Use the tokenizer's chat template to format the message
    messages = [
        {
            "role": "system",
            "content": "You are a friendly chatbot who is an expert in content about York University",
        },
        {"role": "user", "content": question},
    ]

    # Prepare the messages for the model
    input_ids = tokenizer.apply_chat_template(messages, truncation=True, add_generation_prompt=True, return_tensors="pt").to("cuda")

    # Generate a response
    with torch.no_grad():
        outputs = model.generate(
            input_ids=input_ids,
            max_new_tokens=2000,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
        )

    # Decode the generated tokens and return the response
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return jsonify({'answer': response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
