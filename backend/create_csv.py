import csv
import os

"""
base dictionary with farm_id as key
outline:
dic = {
    "farm_id": {
        "irrigation": {
            "irrigation_inches": [],
            "dates": ['10/24/2024']
        },
        "plot_id": [""],  # Plot ID
        "soil_info": [
            {
                "depth": "", # depth in inches
                "OMC": "", 
                "soil_texture_class": ""
            }
        ],
        "soil_ph": "",
        "weather": {
            "percipitation": "",
            "humidity": "",
            "fahrenheit" : "",
        }
    }
}
"""
dic = {
    "24": {
        "plot_id": ["2701", "2606", "1202", "804"],
        "soil_info": []
    },
    "13": {
        "plot_id": ["2702", "1704", "1201", "405"],
        "soil_info": []
    },
    "1": {
        "plot_id": ["2703", "2005", "1204", "201"],
        "soil_info": []
    },
    "2": {
        "plot_id": ["2704", "1903", "602", "205"],
        "soil_info": []
    },
    "34": {
        "plot_id": ["2705", "1603", "902", "504"],
        "soil_info": []
    },
    "35": {
        "plot_id": ["2706", "1702"],
        "soil_info": []
    },
    "23": {
        "plot_id": ["2601", "1904", "1306", "603"],
        "soil_info": []
    },
    "17": {
        "plot_id": ["2602", "2205", "606", "503"],
        "soil_info": []
    },
    "26": {
        "plot_id": ["2603", "2406", "605", "202"],
        "soil_info": []
    },
    "28": {
        "plot_id": ["2604", "2003", "1302", "406"],
        "soil_info": []
    },
    "30": {
        "plot_id": ["2605", "2302", "1301", "206"],
        "soil_info": []
    },
    "19": {
        "plot_id": ["2501", "1906", "502", "305"],
        "soil_info": []
    },
    "15": {
        "plot_id": ["2502", "2206", "903", "404"],
        "soil_info": []
    },
    "8": {
        "plot_id": ["2503", "1804", "601", "506"],
        "soil_info": []
    },
    "5": {
        "plot_id": ["2504", "2303", "505", "301"],
        "soil_info": []
    },
    "7": {
        "plot_id": ["2505", "1803", "1006", "901"],
        "soil_info": []
    },
    "12": {
        "plot_id": ["2506", "2203", "805", "402"],
        "soil_info": []
    },
    "10": {
        "plot_id": ["2401", "1706", "604", "303"],
        "soil_info": []
    },
    "11": {
        "plot_id": ["2402", "2404", "906", "801"],
        "soil_info": []
    },
    "21": {
        "plot_id": ["2403", "1705", "1001", "306"],
        "soil_info": []
    },
    "20": {
        "plot_id": ["2405", "1501", "806", "302"],
        "soil_info": []
    },
    "4": {
        "plot_id": ["2301", "1806", "1102", "304"],
        "soil_info": []
    },
    "25": {
        "plot_id": ["2304", "1801", "1106", "403"],
        "soil_info": []
    },
    "33": {
        "plot_id": ["2305", "1703", "1504", "1002"],
        "soil_info": []
    },
    "27": {
        "plot_id": ["2306", "2202", "1303", "204"],
        "soil_info": []
    },
    "9": {
        "plot_id": ["2201", "1503", "1506", "1104"],
        "soil_info": []
    },
    "16": {
        "plot_id": ["2204", "2002", "1105", "1003"],
        "soil_info": []
    },
    "6": {
        "plot_id": ["2001", "1606", "905", "802"],
        "soil_info": []
    },
    "3": {
        "plot_id": ["2004", "1502", "1005", "501"],
        "soil_info": []
    },
    "29": {
        "plot_id": ["2006", "1902", "1205", "1103"],
        "soil_info": []
    },
    "22": {
        "plot_id": ["1901", "1604", "1305", "1203"],
        "soil_info": []
    },
    "31": {
        "plot_id": ["1905", "1601", "1004", "803"],
        "soil_info": []
    },
    "18": {
        "plot_id": ["1802", "1805", "1206", "1101"],
        "soil_info": []
    },
    "14": {
        "plot_id": ["1701", "1605", "1304", "203"],
        "soil_info": []
    },
    "32": {
        "plot_id": ["1602", "1505", "904", "401"],
        "soil_info": []
    }
}


def farm_id_to_irrigation(filepath):
    try:
        with open(filepath, mode='r') as file:
            csvFile = csv.reader(file)
            dates = []
            for i, row in enumerate(csvFile):
                if i == 0:
                    continue

                if i == 1:
                    dates = row[1:]

                else:
                    if row[0] in dic:
                        dic[row[0]]["irrigation"] = {
                            "irrigation_inches": row[1:-1],
                            "dates": dates
                        }
                    else:
                        dic[row[0]] = {
                            "irrigation": {
                                "irrigation_inches": row[1:-1],
                                "dates": dates
                            }
                        }
            
    except Exception as e:
        print(str(e))

def shallow_soil_sampling_data(filepath):
    def create_entry(row, add_plot_id=False):
        if add_plot_id:
            return {
                "plot_id": row[1],
                "soil_ph": row[5],
            }
        else:
            return {
                "soil_ph": row[5],
            }
    try:
        with open(filepath, mode='r') as file:
            csvFile = csv.reader(file)
            for i, row in enumerate(csvFile):
                if i == 0 or i == 1:
                    continue
                else:
                    if row[0] in dic:
                        # Update the existing entry with new values
                        dic[row[0]].update(create_entry(row))
                    else:
                        print("DIDNT FIND: ", row[0])
                        # Create a new entry if not seen
                        dic[row[0]] = create_entry(row, True)      
    except Exception as e:
        print(str(e))

def arable_data(team_number, filepath):
    with open(filepath, mode='r') as file:
            csvFile = csv.reader(file)
            dic[team_number][""]
            for i, row in enumerate(csvFile):
                if i == 0 or i == 1:
                    print("skipping these: ", row[0])
                    continue
                
                dic[team_number][0]

def soil_texture_data(filepath):
    with open(filepath, mode='r') as file:
        csvFile = csv.reader(file)
        for i, row in enumerate(csvFile):
            if i == 0 or i == 1:
                continue
                
            for key, value in dic.items():
                if row[0] in value["plot_id"]:
                    dic[key]["soil_info"].append({
                        "depth": row[5],
                        "OMC": row[6],
                        "soil_texture_class": row[7]
                    })

def write_to_csv():
    # change to your local url
    file_path = os.path.join(r".\backend", "plots_data.csv")

    with open(file_path, mode="w", newline='') as file:
        fieldnames = ["farm_id", "plot_ids", ""]

def main():
    # create farm_id to irrigation
    farm_id_to_irrigation(r"./2024_TAPS_management(Irrigation amounts).csv")
    
    # create shallow soil sample data
    shallow_soil_sampling_data(r"./24 KSU TAPS Shallow soil sampling(Sheet1).csv")

    # this class is finding no matches?? maybe this data is just relative for the field??
    # raw_spatial_data(r"C:\Users\kevin\Downloads\2024_TAPS_Veris_raw_spatial_data(pH).csv")

    # create soil texture data
    soil_texture_data(r"./24 KSU TAPS Soil texture(data).csv")

    try:
        for key, value in dic.items():
            print(key, ": ", value)
            print("\n")
    except Exception as e:
        print(str(e))
    
    return dic