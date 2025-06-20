from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
import requests
import os
load_dotenv()

app = Flask(__name__)

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({'error': 'No message provided'}), 400

        headers = {
            'Authorization': f'Bearer {GROQ_API_KEY}',
            'Content-Type': 'application/json'
        }

        payload = {
            'model': 'llama3-8b-8192',
            'messages': [
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': user_message}
            ],
            'max_tokens': 256
        }

        response = requests.post('https://api.groq.com/openai/v1/chat/completions', 
                              headers=headers, 
                              json=payload)

        if response.status_code != 200:
            return jsonify({'error': f'API error: {response.status_code}'}), 500

        response_data = response.json()
        bot_response = response_data['choices'][0]['message']['content']
        return jsonify({'response': bot_response})

    except Exception as e:
        print(f'Error: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)