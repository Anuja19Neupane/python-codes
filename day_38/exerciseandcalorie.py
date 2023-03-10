import requests
from datetime import datetime
import os
# os is in standard library no need to install.

#cwd=os.getcwd()
#print(cwd)

GENDER = "female"
WEIGHT_KG = 45
HEIGHT_CM =156
AGE = 18

#print(os.environ["PATH"])
#print(os.environ["DEBUG"])


APP_ID = os.environ["YOUR_APP_ID"]
API_KEY = os.environ["YOUR_API_KEY"]
# os.environ in Python is a mapping object that represents the user’s environmental variables.
#  It returns a dictionary having user’s environmental variable as key and their values as value.

# Return Type: This returns a dictionary representing the user’s environmental variables

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"
sheet_endpoint = os.environ["YOUR_SHEET_ENDPOINT"]

exercise_text = input("Tell me which exercises you did: ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(result)

today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")
# in hours

for exercise in result["exercises"]:
    sheet_inputs = {
        "workout": {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    
    #sheet_response = requests.post(sheet_endpoint, json=sheet_inputs)


    
    sheet_response = requests.post(
        sheet_endpoint, 
        json=sheet_inputs, 
        auth=(
            os.environ["USERNAME"], 
            os.environ["PASSWORD"],
        )
    )

    bearer_headers = {
    "Authorization": f"Bearer {os.environ['TOKEN']}"
    }
    sheet_response = requests.post(
        sheet_endpoint, 
        json=sheet_inputs, 
        headers=bearer_headers
    )

    print(sheet_response.text)
