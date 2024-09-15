from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_cors import CORS
from db import faqs_collection, users_collection
from bson import ObjectId
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Enable CORS
CORS(app)

# Initialize Bcrypt and JWT
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Secret key for JWT
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

# User Registration
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Check if username already exists
    if users_collection.find_one({"username": username}):
        return jsonify({"error": "Username already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = {"username": username, "password": hashed_password}
    users_collection.insert_one(new_user)
    return jsonify({"message": "User created"}), 201

# User Login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = users_collection.find_one({"username": username})
    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid username or password"}), 401

    access_token = create_access_token(identity=str(user['_id']))
    return jsonify(access_token=access_token), 200

# GET /faqs
@app.route('/faqs', methods=['GET'])
# @jwt_required()
def get_faqs():
    faqs = list(faqs_collection.find({}))
    for faq in faqs:
        faq['_id'] = str(faq['_id'])  # Convert ObjectId to string
    return jsonify(faqs)

# GET /faqs/:id
@app.route('/faqs/<id>', methods=['GET'])
def get_faq(id):
    faq = faqs_collection.find_one({"_id": ObjectId(id)})
    if faq:
        faq['_id'] = str(faq['_id'])  # Convert ObjectId to string
        return jsonify(faq)
    return jsonify({"error": "FAQ not found"}), 404

# POST /faqs
@app.route('/faqs', methods=['POST'])
# @jwt_required()
def create_faq():
    data = request.json
    new_faq = {
        "image": data.get('image'),
        "imageName": data.get('imageName'),  # Include imageName
        "question": data.get('question'),
        "answer": data.get('answer')
    }
    result = faqs_collection.insert_one(new_faq)
    new_faq['_id'] = str(result.inserted_id)  # Convert ObjectId to string
    return jsonify(new_faq), 201

# PUT /faqs/:id
@app.route('/faqs/<id>', methods=['PUT'])
@jwt_required()
def update_faq(id):
    data = request.json
    updated_faq = {
        "image": data.get('image'),
        "imageName": data.get('imageName'),  # Include imageName
        "question": data.get('question'),
        "answer": data.get('answer')
    }
    result = faqs_collection.update_one({"_id": ObjectId(id)}, {"$set": updated_faq})
    if result.modified_count > 0:
        updated_faq['_id'] = id  # Ensure _id is included in the response
        return jsonify(updated_faq)
    return jsonify({"error": "FAQ not found"}), 404

# DELETE /faqs/:id
@app.route('/faqs/<id>', methods=['DELETE'])
@jwt_required()
def delete_faq(id):
    result = faqs_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return jsonify({"message": "FAQ deleted"})
    return jsonify({"error": "FAQ not found"}), 404

# Language detection
@app.route('/api/detect', methods=['POST'])
def detect_language():
    data = request.get_json()
    text = data.get('text')

    url = 'https://google-translator9.p.rapidapi.com/v2/detect'
    headers = {
        'x-rapidapi-key': os.getenv('RAPIDAPI_KEY'),
        'x-rapidapi-host': 'google-translator9.p.rapidapi.com',
        'Content-Type': 'application/json'
    }
    payload = {
        'q': text
    }

    response = requests.post(url, json=payload, headers=headers)
    return jsonify(response.json())

# Text translation
@app.route('/api/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    text = data.get('text')
    target_lang = data.get('targetLang')

    url = 'https://google-translator9.p.rapidapi.com/v2'
    headers = {
        'x-rapidapi-key': os.getenv('RAPIDAPI_KEY'),
        'x-rapidapi-host': 'google-translator9.p.rapidapi.com',
        'Content-Type': 'application/json'
    }
    payload = {
        'q': text,
        'target': target_lang
    }

    response = requests.post(url, json=payload, headers=headers)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run()
