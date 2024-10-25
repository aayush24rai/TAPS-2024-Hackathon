from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect 
from create_csv import farm_id_to_irrigation

app = Flask(__name__)
CORS(app)
csrf = CSRFProtect(app)

@app.route('/login', methods=["POST"])
@csrf.exempt
def login():
    return jsonify({})

def main():
    dic = farm_id_to_irrigation(r"C:\Users\kevin\Downloads\2024_TAPS_management(Irrigation amounts).csv")

    answer = "y"
    while answer == "y":
        id = input("Enter a farm id: ")
        print(dic[id])

        answer = input("continue? ")

main()