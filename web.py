from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

# JWT Configuration
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this in production!
jwt = JWTManager(app)

# In-memory user store (use a real database in production)
users = {
    "testuser": generate_password_hash("password")
}

@app.route("/", methods=["GET"])
def home():
    return jsonify({"msg": "Welcome to the Flask app!"})

@app.route("/register", methods=["POST"])
def register():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    if username in users:
        return jsonify({"msg": "Username already exists"}), 400

    users[username] = generate_password_hash(password)
    return jsonify({"msg": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    if username not in users or not check_password_hash(users[username], password):
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
