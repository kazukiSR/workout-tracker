import requests
import os
from datetime import datetime

GENDER = "male"
WEIGHT_KG = 63.50
HEIGHT_CM = 175.0
AGE = 19

APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]

ENDPOINT = "https://trackapi.nutritionix.com"
exercisePost = f"{ENDPOINT}/v2/natural/exercise"

SHEETY_ENPOINT = os.environ["SHEETY_ENPOINT"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]

bearerTokenSheety = f"Bearer {BEARER_TOKEN}"


nutritionHeaders = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

sheetyHeaders = {
    "Authorization": bearerTokenSheety
}

exerciseText = input("What did you do today?: ")

exerciseJson = {
    "query": exerciseText,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE,
}

response = requests.post(url=exercisePost, json=exerciseJson, headers=nutritionHeaders)
result = response.json()
print(result)
todayDate = datetime.now().strftime("%d/%m/%Y")
nowTime = datetime.now().strftime("%X")

for exercise in result["exercises"]:
    sheetInput = {
        "workout": {
            "date": todayDate,
            "time": nowTime,
            "exercise": exercise['name'].title(),
            "duration": exercise['duration_min'],
            "calories": exercise['nf_calories'],
        }
    }
    sheetResponse = requests.post(url=SHEETY_ENPOINT, json=sheetInput, headers=sheetyHeaders)
    print(sheetResponse.text)


