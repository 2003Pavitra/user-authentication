from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import os  # ✅ Needed for os.environ

app = Flask(__name__)

# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this to a more secure key in production!
jwt = JWTManager(app)

# In a real app, you'd store users in a database
users = {
    "testuser": generate_password_hash("password")
}

# Root route to avoid 404 errors when accessing "/"
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

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
