from flask import Flask, request, jsonify 
from flask_cors import CORS
import requests
import base64
from flask import Flask, render_template, request
import pandas as pd
import joblib

app = Flask(__name__)
CORS(app)
clustering_model = joblib.load('clustering.joblib')
label_encoder = joblib.load('label_encoder.joblib')
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

@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the uploaded file
    uploaded_file = request.files['file']

    if uploaded_file:
        # Load the user-uploaded data into a DataFrame
        user_data = pd.read_csv(uploaded_file)
        print(user_data)

        # Check if the required column is present in the user-uploaded data
        if 'Gender' in user_data.columns:
            # Apply label encoding to the relevant column
            
            user_data['Gender'] = label_encoder.transform(user_data['Gender'])
            
            # Use the clustering model to make predictions
            predictions = clustering_model.predict(user_data)

            # Optionally, you can return or process the predictions as needed
            return f"Predictions: {predictions}"

        else:
            return "Error: 'Category' column not found in the uploaded file."

    return "Error: No file uploaded."


if __name__ == "__main__":
  app.run() 