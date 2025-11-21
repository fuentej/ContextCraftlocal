"""
{project_name} - Flask Application
Created: {date}
"""

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

@app.route('/')
def home():
    return jsonify({{"message": "Hello from {project_name}!"}})

@app.route('/health')
def health_check():
    return jsonify({{"status": "healthy"}})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8000)
