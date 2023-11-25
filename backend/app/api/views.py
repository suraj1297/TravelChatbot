from flask import Blueprint, jsonify, request
from ..services.GatewayPredicter import Predict
from joblib import load
import os
from openai import OpenAI
import numpy as np

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/gateway', methods=['POST'])
def gateway():
    if request.is_json:
        data = request.get_json()
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        current_dir = os.path.dirname(__file__)
        model_path = os.path.join(current_dir, '..', 'ml_model', 'gateway_classifier.joblib')
        model = load(model_path)
        vector = client.embeddings.create(input = data["input_data"], model='text-embedding-ada-002').data[0].embedding
        vector = np.array(vector).reshape(1, -1)
        prediction = model.predict(vector)
        return jsonify({"message": str(prediction[0])}), 200
    else:
        return jsonify({"error": "Request must be JSON"}), 400

