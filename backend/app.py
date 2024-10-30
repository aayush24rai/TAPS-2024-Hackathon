from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect 
from create_csv import main
from create_pdf import create_pdf
from datetime import datetime, timedelta
from threading import Thread, Event
import numpy as np
import requests

app = Flask(__name__)
CORS(app)
csrf = CSRFProtect(app)

dic = {}
initialize_dictionary_event = Event()
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
    
    # for i, day in enumerate(week_weather):
    #     print(f"DAY {i}: ", day)
    #     print("\n")
    
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
    
def calculate_evapotransporation(precipitation, avg_temp, max_temp, min_temp, avg_humidity, irrigation_mm):
    # Potential Evapotranspiration for the week
    PET = 0.0023 * (avg_temp + 17.8) * ((max_temp - min_temp) ** 0.5) 
    print("PET: ", PET)

    # Humidity adjustment
    humidity_adjustment = (100 - avg_humidity) / 100
    print("HUMIDIDTY ADJUSTMENT: ", humidity_adjustment)

    # Adjust with humidity
    adjusted_pet = PET * humidity_adjustment
    print("AFJUSTED PET: ", adjusted_pet)

    print("IRRIGATION MM: ", irrigation_mm)

    print("PRECIPITATION : ", precipitation)
    # Actual Evapotranspiration
    AET = adjusted_pet - precipitation + irrigation_mm

    return AET

def water_needed_for_crop (AET, effective_rainfall):
    # Irrigation water needed
    return (AET - effective_rainfall) / 25.4

def calculate_money_saved(irrigation_optimized_mm, irrigation_given_mm):
    """
    Calculate money and water saved through irrigation optimization.
    
    Args:
        irrigation_optimized_mm (float): Optimized irrigation amount in millimeters
        irrigation_given_mm (float): Current irrigation amount in millimeters
    
    Returns:
        dict: Dictionary containing money saved and water usage data for both single plot
             and entire farm conversion
    """
    print("\n\n\n\nIRRIGATION OPTIMIZED MM: ", irrigation_optimized_mm)
    print("IRRIGATION GIVEN MM: ", irrigation_given_mm)
    # Constants
    AVG_FARM_ACRES = 32.5  # Average farm size in Colby, Kansas = 804 => farmers split irrigation in pivots => pivot size around (130 acres) => weekly irrigated acres is around 1/4 of total pivot
    PLOT_SIZE_ACRES = 0.0413  # Plot size in acres
    SQFT_PER_ACRE = 43560  # Square feet per acre
    MM_TO_FEET = 0.00328084  # Conversion factor from mm to feet
    CUBIC_FT_TO_GALLONS = 7.48  # Conversion factor from cubic feet to gallons
    COST_PER_GALLON = 1.90  # Cost per gallon in dollars
    
    # Calculate farm size conversion factor
    farm_size_conversion = AVG_FARM_ACRES / PLOT_SIZE_ACRES
    
    # Convert irrigation amounts from mm to feet
    irrigation_given_ft = irrigation_given_mm * MM_TO_FEET
    irrigation_optimized_ft = irrigation_optimized_mm * MM_TO_FEET
    
    print("IRRIGATION GIVEN FT: ", irrigation_given_ft)
    print("IRRIGATION OPTIMIZED FT: ",  irrigation_optimized_ft)

    # Convert to volume in cubic feet (area * height)
    plot_area_sqft = PLOT_SIZE_ACRES * SQFT_PER_ACRE
    irrigation_given_cuft = irrigation_given_ft * plot_area_sqft
    irrigation_optimized_cuft = irrigation_optimized_ft * plot_area_sqft

    print("IRRIGATION GIVEN VOLUME: ", irrigation_given_cuft)
    print("IRRIGATION OPTIMIZED VOLUME: ", irrigation_optimized_cuft)
    
    # Convert cubic feet to gallons
    irrigation_given_gallons = irrigation_given_cuft * CUBIC_FT_TO_GALLONS
    irrigation_optimized_gallons = irrigation_optimized_cuft * CUBIC_FT_TO_GALLONS

    print("IRRIGATION GIVEN GALLONS: ", irrigation_given_gallons)
    print("IRRIGATION OPTIMIZED GALLONS: ", irrigation_optimized_gallons)
    
    # Calculate costs
    cost_given = irrigation_given_gallons * COST_PER_GALLON
    cost_optimized = irrigation_optimized_gallons * COST_PER_GALLON

    print("COST GIVEN: ", cost_given)
    print("COST OPTIMZIED: ", cost_optimized)
    plot_money_saved = cost_given - cost_optimized
    print("PLOT MONEY SAVED: ", plot_money_saved)
    
    # Prepare return values with farm-wide conversions
    return {
        "converted_money_saved": round(farm_size_conversion * plot_money_saved, 2),
        "plot_money_saved": round(plot_money_saved, 2),
        "converted_irrigation_given_gallons": round(farm_size_conversion * irrigation_given_gallons, 2),
        "converted_irrigation_optimized_gallons": round(farm_size_conversion * irrigation_optimized_gallons, 2),
        "plot_irrigation_given_gallons": round(irrigation_given_gallons, 2),
        "plot_irrigation_optimized_gallons": round(irrigation_optimized_gallons, 2)
    }

# return killowat-hours saved 
def calculate_energy_saved(converted_given_gallons, converted_optimized_gallons, given_gallons, optimized_gallons):
    # assume a general energy intensity factor, such as XkWh per 1000 gallons
    converted_energy = (converted_given_gallons - converted_optimized_gallons) / 100 * 1.5
    optimized_energy = (given_gallons - optimized_gallons) / 100 * 1.5
    return {
        "converted_optimized_energy": round(converted_energy, 2),
        "plot_optimized_energy": round(optimized_energy, 2)
    }


@app.route('/get/plot/info', methods=["POST"])
@csrf.exempt
def testing():
    try:
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

        week_number = 12
        farm_id = request.form.get("farm_id")
        
        print("FARM ID: ", farm_id)
        if farm_id:
            # Handle irrigation retrieval safely
            if week_number < len(dic[farm_id]["irrigation"]["irrigation_inches"]):
                irrigation_inches = dic[farm_id]["irrigation"]["irrigation_inches"][week_number]
            else:
                irrigation_inches = 0

            irrigation_inches = float(irrigation_inches)
            print("IRRIGATION INCHES: ", irrigation_inches)
            irrigation_mm = irrigation_inches * 25.4
            irrigation_mm = round(irrigation_mm, 2)

            evapotransporation = calculate_evapotransporation(precipitation, avg_temp, max_temp, min_temp, avg_humidity, irrigation_mm)
            print("EVAPOTRANSPORATION: ", evapotransporation)

            optimal_irrigation_inches = water_needed_for_crop(evapotransporation, effective_rainfall)
            optimal_irrigation_inches = round(optimal_irrigation_inches, 2)
            optimal_irrigation_mm = optimal_irrigation_inches * 25.4
            print("OPTIMAL IRRIGATION IN INCHES: ", optimal_irrigation_mm)

            money_info = calculate_money_saved(optimal_irrigation_mm, irrigation_mm)
            energy_info = calculate_energy_saved(money_info["converted_irrigation_given_gallons"], money_info["converted_irrigation_optimized_gallons"], money_info["plot_irrigation_given_gallons"], money_info["plot_irrigation_optimized_gallons"])

            email = request.form.get("email")

            thread = Thread(target=create_pdf, args=(email, optimal_irrigation_inches, farm_id, money_info, energy_info, week_weather))
            thread.start()

            return jsonify({
                "status": 200,
                "optimal_irrigation": optimal_irrigation_mm,
                "given_irrigation": irrigation_inches,
                "money_info": money_info,
                "energy_info": energy_info,
                "weather_data": week_weather
            })
        else:
            return jsonify({
                "status": 404,
                "message": "Could not find farm_id"
            })
    
    except Exception as e:
        return jsonify({
            "status": 500,
            "message": str(e)
        })