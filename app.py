from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

print("Running Flask App...")

# Load your fine-tuned model using the pipeline API
model_path = "data/zephyr-7b-sft-lora"  # Adjust the path as necessary or use the model identifier if it's uploaded to the Hugging Face Model Hub
text_generation_pipeline = pipeline("text-generation", model=model_path)  # Set device=0 to run on GPU, or remove for CPU

@app.route('/Answer', methods=['POST'])
def answer():
    data = request.json
    question = data.get('question', '')

    # Prepare the prompt with the system and user messages
    prompt = f"You are a friendly chatbot who is an expert in content about York University\n\nUser: {question}\nBot:"
    
    # Generate the response using the pipeline
    response = text_generation_pipeline(prompt, max_length=512, clean_up_tokenization_spaces=True)[0]['generated_text']
    
    # Extract just the Bot's response
    bot_response = response.split("Bot:")[-1].strip()

    return jsonify({'answer': bot_response})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
