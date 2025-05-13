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
  /* Styling as per modern mobile-friendly design */
  * { box-sizing: border-box; }
  body {
    margin: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: #333; min-height: 100vh;
    display: flex; flex-direction: column; align-items: center; padding: 1rem;
  }
  h1 { color: white; margin-bottom: 0.25rem; }
  main {
    background: white;
    width: 100%; max-width: 380px;
    border-radius: 12px;
    box-shadow: 0 6px 15px rgba(0,0,0,0.15);
    padding: 2rem; margin-top: 10px;
  }
  form {
    display: flex; flex-direction: column;
  }
  label {
    margin: 1rem 0 0.3rem 0; font-weight: 600;
  }
  input[type="text"], input[type="password"] {
    padding: 0.5rem 0.75rem; font-size: 1rem;
    border: 2px solid #ddd; border-radius: 8px;
    transition: border-color 0.3s ease;
  }
  input[type="text"]:focus, input[type="password"]:focus {
    outline: none; border-color: #667eea;
  }
  button {
    margin-top: 1.5rem;
    padding: 0.7rem 1rem;
    font-size: 1.1rem; font-weight: 700;
    border: none; border-radius: 8px;
    cursor: pointer; background-color: #667eea;
    color: white; transition: background-color 0.3s ease;
  }
  button:hover:not(:disabled) {
    background-color: #5563c1;
  }
  button:disabled {
    background-color: #aaa;
    cursor: not-allowed;
  }
  nav {
    display: flex; gap: 10px; justify-content: center; margin-bottom: 10px;
  }
  nav button {
    flex: 1 1 50%;
  }
  .message {
    margin-top: 1rem; font-weight: 600; min-height: 24px;
  }
  .message.success { color: #2c7a2c; }
  .message.error { color: #b53a3a; }
  .protected-section {
    margin-top: 2rem;
    background: #f1f1f1; border-radius: 10px; padding: 1rem;
    font-size: 1.1rem; word-break: break-word;
    color: #222; border: 2px solid #667eea;
    text-align: center;
  }
  @media (max-width: 400px) {
    main { max-width: 100%; padding: 1rem; }
    input[type="text"], input[type="password"] { font-size: 0.9rem; }
    button { font-size: 1rem; padding: 0.6rem; }
  }
</style>
</head>
<body>
  <h1>JWT Authentication</h1>
  <main>
    <nav>
      <button id="btn-show-login" type="button" aria-label="Show login form">Login</button>
      <button id="btn
