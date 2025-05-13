from flask import Flask, jsonify, request, render_template_string
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import os
app = Flask(__name__)
# Setup JWT
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "super-secret")  # set environment var in Render for production
jwt = JWTManager(app)
# In-memory users database (for demonstration only)
users = {
    "testuser": generate_password_hash("password")
}
# Serve the frontend HTML
FRONTEND_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no" />
<title>Flask JWT Auth App</title>
<style>

tell me what this code is for: from flask import Flask, jsonify, request from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(name)

Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "super-secret" # Change this! jwt = JWTManager(app)

In a real app, you'd store users in a database
users = { "testuser": generate_password_hash("password") }

Add this root route to avoid 404 errors when accessing "/"
@app.route("/", methods=["GET"]) def home(): return jsonify({"msg": "Welcome to the Flask app!"})

@app.route("/register", methods=["POST"]) def register(): username =
