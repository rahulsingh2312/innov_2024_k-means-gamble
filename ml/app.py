from flask import Flask, request, jsonify 
from flask_cors import CORS
import requests
import base64

app = Flask(__name__)
CORS(app)

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

@app.route('/generate/image', methods=['POST'])
def generate_code():
    data = request.get_json()
    text = data["text"]
    input = {"inputs": text}
    response = query(input)
    encoded_string = base64.b64encode(response)
    output = {"image": encoded_string.decode("utf-8")}
    return jsonify(output)

if __name__ == "__main__":
  app.run() 