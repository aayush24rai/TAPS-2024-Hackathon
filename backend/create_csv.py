import csv

"""
base dictionary with farm_id as key
outline:
dic = {
    "farm_id": {
        "irrigation": {
            "irrigation_inches": [],
            "dates": ['10/24/2024']
        },
        "plot_id": "",  # Plot ID
        "latitude": 0.0,  # Latitude (floating point)
        "longitude": 0.0,  # Longitude (floating point)
        "sample_id": 0,  # Sample ID
        "soil_ph": 0.0,  # Soil pH
        "excess_lime": "",  # Excess Lime (string or can be boolean depending on data type)
        "organic_matter_percent": 0.0,  # Organic matter (%)
        "nitrate_nitrogen_ppm": 0.0,  # Nitrate-Nitrogen (ppm)
        "nitrate_nitrogen_lbs_per_acre": 0.0,  # Nitrate-Nitrogen (lbs of N/acre)
        "phosphorus_ppm": 0.0,  # Phosphorus (ppm)
        "potassium_ppm": 0.0,  # Potassium (ppm)
        "sulfur_ppm": 0.0,  # Sulfur (ppm)
        "sulfur_lbs_per_acre": 0.0,  # Sulfur (lbs of S/acre)
        "calcium_ppm": 0.0,  # Calcium (ppm)
        "magnesium_ppm": 0.0,  # Magnesium (ppm)
        "sodium_ppm": 0.0,  # Sodium (ppm)
        "zinc_ppm": 0.0,  # Zinc (ppm)
        "iron_ppm": 0.0,  # Iron (ppm)
        "manganese_ppm": 0.0,  # Manganese (ppm)
        "copper_ppm": 0.0,  # Copper (ppm)
        "boron_ppm": 0.0,  # Boron (ppm)
        "cec_meq_per_100g": 0.0,  # Cation Exchange Capacity (CEC) (meq per 100g)
        "cec_k_percent": 0.0,  # CEC K (%)
        "cec_ca_percent": 0.0,  # CEC Ca (%)
        "cec_mg_percent": 0.0,  # CEC Mg (%)
        "cec_na_percent": 0.0  # CEC Na (%),
        "sample": {
            0 : {
                "avg_ph": 0.0    # average pG,
                "pH1": 0.0    # first pH,
                "pH2": 0.0   # second pH,
                "altitude": 900.0   # altitude of plot,
                "speed": 3.0   # speed of plot??
            } # sample number
        }  # array of samples
    }
}
"""
dic = {
    "24": {
        "plot_id": ["2701", "2606", "1202", "804"]
    },
    "13": {
        "plot_id": ["2702", "1704", "1201", "405"]
    },
    "1": {
        "plot_id": ["2703", "2005", "1204", "201"]
    },
    "2": {
        "plot_id": ["2704", "1903", "602", "205"]
    },
    "34": {
        "plot_id": ["2705", "1603", "902", "504"]
    },
    "35": {
        "plot_id": ["2706", "1702"]
    },
    "23": {
        "plot_id": ["2601", "1904", "1306", "603"]
    },
    "17": {
        "plot_id": ["2602", "2205", "606", "503"]
    },
    "26": {
        "plot_id": ["2603", "2406", "605", "202"]
    },
    "28": {
        "plot_id": ["2604", "2003", "1302", "406"]
    },
    "30": {
        "plot_id": ["2605", "2302", "1301", "206"]
    },
    "19": {
        "plot_id": ["2501", "1906", "502", "305"]
    },
    "15": {
        "plot_id": ["2502", "2206", "903", "404"]
    },
    "8": {
        "plot_id": ["2503", "1804", "601", "506"]
    },
    "5": {
        "plot_id": ["2504", "2303", "505", "301"]
    },
    "7": {
        "plot_id": ["2505", "1803", "1006", "901"]
    },
    "12": {
        "plot_id": ["2506", "2203", "805", "402"]
    },
    "10": {
        "plot_id": ["2401", "1706", "604", "303"]
    },
    "11": {
        "plot_id": ["2402", "2404", "906", "801"]
    },
    "21": {
        "plot_id": ["2403", "1705", "1001", "306"]
    },
    "20": {
        "plot_id": ["2405", "1501", "806", "302"]
    },
    "4": {
        "plot_id": ["2301", "1806", "1102", "304"]
    },
    "25": {
        "plot_id": ["2304", "1801", "1106", "403"]
    },
    "33": {
        "plot_id": ["2305", "1703", "1504", "1002"]
    },
    "27": {
        "plot_id": ["2306", "2202", "1303", "204"]
    },
    "9": {
        "plot_id": ["2201", "1503", "1506", "1104"]
    },
    "16": {
        "plot_id": ["2204", "2002", "1105", "1003"]
    },
    "6": {
        "plot_id": ["2001", "1606", "905", "802"]
    },
    "3": {
        "plot_id": ["2004", "1502", "1005", "501"]
    },
    "29": {
        "plot_id": ["2006", "1902", "1205", "1103"]
    },
    "22": {
        "plot_id": ["1901", "1604", "1305", "1203"]
    },
    "31": {
        "plot_id": ["1905", "1601", "1004", "803"]
    },
    "18": {
        "plot_id": ["1802", "1805", "1206", "1101"]
    },
    "14": {
        "plot_id": ["1701", "1605", "1304", "203"]
    },
    "32": {
        "plot_id": ["1602", "1505", "904", "401"]
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
                            "irrigation_inches": row[1:],
                            "dates": dates
                        }
                    else:
                        dic[row[0]] = {
                            "irrigation": {
                                "irrigation_inches": row[1:],
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
                "latitude": row[2],
                "longitude": row[3],
                "sample_id": row[4],
                "soil_ph": row[5],
                "excess_lime": row[6],
                "organic_matter_percent": row[7],
                "nitrate_nitrogen_ppm": row[8],
                "nitrate_nitrogen_lbs_per_acre": row[9],
                "phosphorus_ppm": row[10],
                "potassium_ppm": row[11],
                "sulfur_ppm": row[12],
                "sulfur_lbs_per_acre": row[13],
                "calcium_ppm": row[14],
                "magnesium_ppm": row[15],
                "sodium_ppm": row[16],
                "zinc_ppm": row[17],
                "iron_ppm": row[18],
                "manganese_ppm": row[19],
                "copper_ppm": row[20],
                "boron_ppm": row[21],
                "cec_meq_per_100g": row[22],
                "cec_k_percent": row[23],
                "cec_ca_percent": row[24],
                "cec_mg_percent": row[25],
                "cec_na_percent": row[26]
            }
        else:
            return {
                "latitude": row[2],
                "longitude": row[3],
                "sample_id": row[4],
                "soil_ph": row[5],
                "excess_lime": row[6],
                "organic_matter_percent": row[7],
                "nitrate_nitrogen_ppm": row[8],
                "nitrate_nitrogen_lbs_per_acre": row[9],
                "phosphorus_ppm": row[10],
                "potassium_ppm": row[11],
                "sulfur_ppm": row[12],
                "sulfur_lbs_per_acre": row[13],
                "calcium_ppm": row[14],
                "magnesium_ppm": row[15],
                "sodium_ppm": row[16],
                "zinc_ppm": row[17],
                "iron_ppm": row[18],
                "manganese_ppm": row[19],
                "copper_ppm": row[20],
                "boron_ppm": row[21],
                "cec_meq_per_100g": row[22],
                "cec_k_percent": row[23],
                "cec_ca_percent": row[24],
                "cec_mg_percent": row[25],
                "cec_na_percent": row[26]
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


# this class is finding no matches?? maybe this data is just relative for the field??
def raw_spatial_data(filepath):
    with open(filepath, mode='r') as file:
            csvFile = csv.reader(file)
            for i, row in enumerate(csvFile):
                if i == 0:
                    print("skippting this: ", row[0])
                    continue
                
                for key, value in dic.items():
                    if "sample" not in dic[key]:
                        dic[key]["sample"] = {}
                    if value["longitude"] == row[0] and value["latitude"] == row[1]:
                        dic[key]["sample"][row[7]] = {
                            "avg_ph": row[2],   
                            "pH1": row[3],
                            "pH2": row[4], 
                            "altitude": row[5], 
                            "speed": row[6],
                        }  

def main():
    # create farm_id to irrigation
    farm_id_to_irrigation(r"C:\Users\kevin\Downloads\2024_TAPS_management(Irrigation amounts).csv")
    
    # create shallow soil sample data
    shallow_soil_sampling_data(r"C:\Users\kevin\Downloads\24 KSU TAPS Shallow soil sampling(Sheet1).csv")

    # this class is finding no matches?? maybe this data is just relative for the field??
    # raw_spatial_data(r"C:\Users\kevin\Downloads\2024_TAPS_Veris_raw_spatial_data(pH).csv")

    try:
        for key in dic:
            print(key, ": ", dic[key]["sample"])
            print("\n")
    except Exception as e:
        print(str(e))

main()