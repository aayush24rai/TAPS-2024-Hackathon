from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect 

app = Flask(__name__)
CORS(app)
csrf = CSRFProtect(app)

@app.route('/login', methods=["POST"])
@csrf.exempt
def login():
    return jsonify({})