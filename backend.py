from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

model_path = "data/zephyr-7b-sft-lora"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForCausalLM.from_pretrained(model_path, load_in_4bit=True, device_map="auto")

@app.route('/Answer', methods=['POST'])
def answer():
    data = request.json
    question = data['question']
    response = generate_response(question)
    return jsonify({'answer': response})

def generate_response(question):
    torch.set_grad_enabled(False)
    messages = [
        {"role": "system", "content": "You are a friendly chatbot who is an expert in content about York University"},
        {"role": "user", "content": question},
    ]
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
    app.run(host='0.0.0.0', debug=True)
