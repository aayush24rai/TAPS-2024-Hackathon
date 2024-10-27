from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect 
from create_csv import main
from datetime import datetime, timedelta
from threading import Thread, Event
import numpy as np
import requests

app = Flask(__name__)
CORS(app)
csrf = CSRFProtect(app)

dic = {}
initialize_dictionary_event = Event()
week_to_date = {
    "1": "5/10/2024",
}
weather_key = '5db71530adb34cc0b84212113242710' # get your own weather key from www.weatherapi.com

@app.route('/login', methods=["GET"])
@csrf.exempt
def login():
    try:
        initialize_dictionary_event.clear()  
        thread = Thread(target=initialize_dictionary)
        thread.start()
        return jsonify({
            "status": 200
        })
    except Exception as e:
        return jsonify({
            "status": 500, 
            "error": str(e)
        })
    
@app.route('/get/plot/info', methods=["POST"])
@csrf.exempt
def get_plot_info():
    farm_id = request.form.get("farm_id")
    try:
        initialize_dictionary_event.wait()
        return jsonify(dic[farm_id])
    except Exception as e:
        print(str(e))
        return jsonify({
            "status": 500,
            "message": str(e)
        })
""" 

"""

"""
Keyword arguments:
date: format => yyyy-MM-dd format (i.e. dt=2010-01-01)
city: format => Colby,KS  (no spaces)
"""
def get_weather(start_date, city):
    week_weather = []
    for i in range(7):
        date = (datetime.strptime(start_date, "%Y-%m-%d") + timedelta(days=i)).strftime("%Y-%m-%d")
        url = f"http://api.weatherapi.com/v1/history.json?key={weather_key}&q={city}&dt={date}"
        response = requests.get(url)

        if response.status_code == 200:
            weather_data = response.json()
            day = weather_data["forecast"]["forecastday"][0]["day"]
            
            # change f to c if you want celsius
            week_weather.append({
                "max_temp_f": day["maxtemp_f"],
                "min_temp_f": day["mintemp_f"],
                "avg_temp_f": day["avgtemp_f"],
                "total_precip_mm": day["totalprecip_mm"],
                "avg_humidity": day["avghumidity"],
                "text": day["condition"]["text"]
            })

        else:
            print(f"Error: {response.status_code} - {response.text}")
            return 500
    
    for i, day in enumerate(week_weather):
        print(f"DAY {i}: ", day)
        print("\n")
    
    return week_weather

def initialize_dictionary():
    global dic
    dic = main()
    initialize_dictionary_event.set()

def testing():
    week_weather = get_weather("2024-05-25", "Colby,KS")
