from flask import Flask, request, jsonify 
from flask_cors import CORS
import requests
import base64
from flask import Flask, render_template, request
import pandas as pd
import joblib

clustering_model = joblib.load('clustering.joblib')
encoder = joblib.load('encoder.joblib')

import brochure_generator 

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

@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the uploaded file
    uploaded_file = request.files['file']

    if uploaded_file:
        # Load the user-uploaded data into a DataFrame
        user_data = pd.read_csv(uploaded_file)
        user_data = user_data.drop(columns='CustomerID')
        # print(user_data)
        # Check if the required column is present in the user-uploaded data
        if 'Gender' in user_data.columns:
            # Apply label encoding to the relevant column
            gender_data = user_data[['Gender']]
            # Apply OneHotEncoder to the 'Gender' column
            encoded_gender = encoder.transform(gender_data)
            # print(encoded_gender.toarray())
            to_arr=encoded_gender.toarray()
            # Assign the transformed data back to the 'Gender' column in user_data
            user_data['Gender'] = to_arr[:,0]
            # print(to_arr[:,0])
            # print(user_data)
            # Use the clustering model to make predictions
            predictions = clustering_model.predict(user_data)
            # Optionally, you can return or process the predictions as needed
            output = {"predictions": predictions.tolist()}
            return jsonify(output)

        else:
            return "Error: 'Category' column not found in the uploaded file."

    return "Error: No file uploaded."

app.route('/generate/brochure', methods=['POST'])
def generate_brochure():
    data = request.get_json()
    return brochure_generator.generate_brochure(data["product"], data["age_group"])

if __name__ == "__main__":
  app.run() 