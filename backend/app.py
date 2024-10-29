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

def calculate_effective_rainfall(precipitation):
    """
    Calculate effective rainfall based on total precipitation.
    Effective rainfall = total rainfall - runoff - evaporation - percolation (simplified).
    
    If total precipitation exceeds a certain threshold, the effective rainfall is calculated
    with a different coefficient.
    """
    # Ensure precipitation is in the appropriate unit (e.g., inches)
    
    if precipitation > 18.75:
        # Assuming the 0.8 factor is for higher rainfall scenarios
        return 0.8 * precipitation  # Modify if necessary (like * 25 if converting units)
    
    # For lower rainfall scenarios
    return 0.6 * precipitation  # Modify if necessary (like * 10 if converting units)
    
def calculate_evapotransporation(num_days, precipitation, avg_temp, max_temp, min_temp, avg_humidity, farm_id, week_number):
    # Potential Evapotranspiration for the week
    PET = 0.0023 * (avg_temp + 17.8) * ((max_temp - min_temp) ** 0.5) 
    print("PET: ", PET)

    # Humidity adjustment
    humidity_adjustment = (100 - avg_humidity) / 100
    print("HUMIDIDTY ADJUSTMENT: ", humidity_adjustment)

    # Adjust with humidity
    adjusted_pet = PET * humidity_adjustment
    print("AFJUSTED PET: ", adjusted_pet)

    # Handle irrigation retrieval safely
    if week_number < len(dic[farm_id]["irrigation"]["irrigation_inches"]):
        irrigation_inches = dic[farm_id]["irrigation"]["irrigation_inches"][week_number]
    else:
        irrigation_inches = 0  # Default to 0 or handle accordingly

    irrigation_inches = float(irrigation_inches)
    print("irrigation inches: ", irrigation_inches)

    irrigation_mm = irrigation_inches * 25.4  # Convert to mm
    print("IRRIGATION MM: ", irrigation_mm)

    print("PRECIPITATION : ", precipitation)
    # Actual Evapotranspiration
    AET = adjusted_pet - precipitation + irrigation_mm

    return AET


    
def water_needed_for_crop (AET, effective_rainfall):
    # Irrigation water needed
    return (AET - effective_rainfall) / 25.4


@app.route('/get/plot/info', methods=["POST"])
@csrf.exempt
def testing():
    print("IN TESTING")
    week_weather = get_weather("2024-09-10", "Colby,KS")
    avg_temp = 0
    min_temp = 0
    max_temp = 0
    precipitation = 0
    avg_humidity = 0
    num_days = len(week_weather)

    for i in range(num_days):
        avg_temp += week_weather[i]["avg_temp_f"]
        min_temp += week_weather[i]["min_temp_f"]
        max_temp += week_weather[i]["max_temp_f"]
        avg_humidity += week_weather[i]["avg_humidity"]
        precipitation += week_weather[i]["total_precip_mm"]
    
    # Calculate averages only if there are days
    if num_days > 0:
        avg_temp /= num_days
        min_temp /= num_days
        max_temp /= num_days
        avg_humidity /= num_days

    effective_rainfall = calculate_effective_rainfall(precipitation)
    print("EFFECTIVE RAINFALL: ", effective_rainfall)

    evapotransporation = calculate_evapotransporation(num_days, precipitation, avg_temp, max_temp, min_temp, avg_humidity, "16", 12)
    print("EVAPOTRANSPORATION: ", evapotransporation)

    optimal_irrigation = water_needed_for_crop(evapotransporation, effective_rainfall)
    print("OPTIMAL IRRIGATION: ", optimal_irrigation)

    return jsonify({
        "status": 200,
        "optimal_irrigation": optimal_irrigation
    })