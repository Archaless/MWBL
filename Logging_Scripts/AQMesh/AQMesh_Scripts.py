# Created by Tyler Knapp 2025-10-08
# Collection of functions to interact with the AQMesh API

import json
import requests
import datetime
import pandas as pd

workingDir = '/usr2/MWBL/Data/AQMesh/Scripts/' # Set to your working directory if needed, ensure trailing '/' is included

def export2csv(response, filename):
    df = pd.DataFrame(response.json())
    df.to_csv(filename, encoding='utf-8', sep=',', decimal=".", index=False)

def handle_status(response, printFlag=True):
    status = response.status_code
    if status == 200 or status == 204: # Successful responses, 204 indicates there will be no content returned
        if printFlag == True:  # Set to True to enable printing
            # Print the response
            print("\nRequest successful")
            print(f"{response.text}\n")
        else:
            pass
    else:
        raise Exception(f"Request failed with status code: {response.status_code}, {response.text}")

def get_location_number(fileName):
    # Reads a JSON file and returns the values for 'location_number' if present.
    with open(fileName, 'r') as f:
        data = json.load(f)

    siteLocs = []
    for site in data:
        siteLocs.append(site.get('location_number'))
    return siteLocs

def get_serial_number(fileName):
    # Reads a JSON file and returns the values for 'serial_number' if present.
    with open(fileName, 'r') as f:
        data = json.load(f)

    sensorNums = []
    for site in data:
        sensorNums.append(site.get('serial_number'))
    return sensorNums

def auth_request(username, password, printFlag=False):
    api_url = "https://api.aqmeshdata.net/api/Authenticate"
    auth = {"username":username,"password":password}
    header =  {"Content-Type":"application/json"}
    response = requests.post(api_url, data=json.dumps(auth), headers=header)
    handle_status(response, printFlag)
    try:
        data = response.json()
        token = data.get("token")  # or "access_token" depending on API
        if token:
            if printFlag == True:
                print("Token received:", token)
            # Optionally, save to a file:
            with open(f"{workingDir}token.json", "w") as f:
                f.write(token)
        else: 
            ValueError(f"Token not found in response: {data}")
    except Exception as e:
        print("Failed to parse JSON or extract token:", e)

def asset_request(printFlag=False):
    api_url = "https://api.aqmeshdata.net/api/pods/Assets/"
    # Read the token from file if it exists
    with open(f"{workingDir}token.json", "r") as f:
        token = f.read().strip()
    header = {"Authorization":f"Bearer {token}"}
    response = requests.get(api_url, headers=header)
    handle_status(response, printFlag)
    
    data = response.json() # First poll for location numbers and other info
    if data is None:
        raise ValueError("No data returned from asset request.")
    with open(f"{workingDir}assets.json", "w") as f:
        json.dump(data, f, indent=4)

def next_request(savePath,printFlag=False):
    api_url = "https://api.aqmeshdata.net/api/LocationData/Next/"
    # Read the token from file if it exists
    with open(f"{workingDir}token.json", "r") as f:
        token = f.read().strip()
    header = {"Authorization":f"Bearer {token}"}
    
    siteLocs = get_location_number(f"{workingDir}assets.json") # Extract location number from the poll response
    if siteLocs is None:
        raise ValueError("Location number not found in the response data.")
    if printFlag == True:
        print(f"\nLocation numbers found: {siteLocs}\n")

    # Now pull data for each location number
    datetimeStr = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # Current date for filename
    # Replace location number with device SN
    for location in siteLocs:
        if location == 3773:
            SN = "2451070"
        elif location == 3774:
            SN = "2451071"
        else:
            raise ValueError(f"Unexpected location number found: {location}")

        # First, pull gases:
        pull_url = f"{api_url}{location}/1/01/0" # 1 indicates gases, 01 indicates Celsius and ug/m3, 0 indicates no Ethylene Oxide
        response = requests.get(pull_url, headers=header)
        handle_status(response, printFlag)

        filename = f"{savePath}aqmeshA-{SN}-{datetimeStr}.csv"

        with open(filename, "w") as f:
            while not response.text == "[]": # Keep pulling until no data is returned
                export2csv(response, filename)
                response = requests.get(pull_url, headers=header)
                handle_status(response, printFlag)
        if printFlag == True:
            print(f"Data saved to {filename}")
        
        # Second, pull particles:
        pull_url = f"{api_url}{location}/2/01/1" # 2 indicates particles, 01 indicates Celsius and ug/m3, 1 includes TPC
        response = requests.get(pull_url, headers=header)
        handle_status(response, printFlag)

        filename = f"{savePath}aqmeshP-{SN}-{datetimeStr}.csv"
        with open(filename, "w") as f:
            while not response.text == "[]": # Keep pulling until no data is returned
                export2csv(response, filename)
                response = requests.get(pull_url, headers=header)
                handle_status(response, printFlag)
        if printFlag == True:
            print(f"Data saved to {filename}")

def repeat_request(savePath,printFlag=False):
    api_url = "https://api.aqmeshdata.net/api/LocationData/Repeat/"
    # Read the token from file if it exists
    with open("./token.json", "r") as f:
        token = f.read().strip()
    header = {"Authorization":f"Bearer {token}"}
    
    siteLocs = get_location_number(f"{workingDir}assets.json") # Extract location number from the poll response
    if siteLocs is None:
        raise ValueError("Location number not found in the response data.")
    if printFlag == True:
        print(f"\nLocation numbers found: {siteLocs}\n")

    # Now pull data for each location number
    datetimeStr = datetime.datetime.now().strftime("%Y%m%d%H%M%S") # Current date for filename
    for location in siteLocs:
        # First pull gases:
        pull_url = f"{api_url}{location}/1/01/0" # 1 indicates gases, 01 indicates Celsius and ug/m3, 0 indicates no Ethylene Oxide
        response = requests.get(pull_url, headers=header)
        handle_status(response, printFlag)

        filename = f"{savePath}AQMesh_{location}_Gas_{datetimeStr}_repeat.csv"
        with open(filename, "w") as f:
            export2csv(response, filename)
        
        # Second pull particles:
        pull_url = f"{api_url}{location}/2/01/1" # 2 indicates particles, 01 indicates Celsius and ug/m3, 1 includes TPC
        response = requests.get(pull_url, headers=header)
        handle_status(response, printFlag)

        filename = f"{savePath}AQMesh_{location}_Particle_{datetimeStr}_repeat.csv"
        with open(filename, "w") as f:
            export2csv(response, filename)

def SD_request(printFlag=False):
    api_url = "https://api.aqmeshdata.net/api/sensor/SensorDetail/1"
    # Read the token from file if it exists
    with open(f"{workingDir}token.json", "r") as f:
        token = f.read().strip()
    header = {"Authorization":f"Bearer {token}"}
    response = requests.get(api_url, headers=header)
    handle_status(response, printFlag)

    data = response.json() # First poll for location numbers and other info
    with open(f"{workingDir}sensors.json", "w") as f:
        json.dump(data, f, indent=4)

def PF_request(printFlag=False):
    api_url = "https://api.aqmeshdata.net/api/Pods/PodFrequencies"
    # Read the token from file if it exists
    with open(f"{workingDir}token.json", "r") as f:
        token = f.read().strip()
    header = {"Authorization":f"Bearer {token}"}
    
    sensorNums = get_serial_number(f"{workingDir}assets.json") # Extract serial numbers from the asset response
    if sensorNums is None:
        raise ValueError("Sensor number not found in the response data.")
    if printFlag == True:
        print(f"Sensor numbers found: {sensorNums}")

    # Now pull data for each location number
    for SN in sensorNums:
        body = {
            "Serial_Number":SN,
            "Particle_P1":"30",
            "Gas_P1":"5",
            "Pod_P2":"900",
            "Pod_P3":"3600"
        }
        response = requests.patch(api_url, headers=header, json=body)
        handle_status(response, printFlag)