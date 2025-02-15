from fastapi import FastAPI, Body
import joblib
import pandas as pd
from pydantic import BaseModel
from typing import List

# Load trained model
model_data = joblib.load("/app/et0/et0_model.pkl")
# model = model_data["model"]
# correct_feature_order = model_data["features"]  # Ensures correct input order
# print(type(model_data))  # What type of object is it?
# print(model_data)  # Print to check content
# Initialize FastAPI

app = FastAPI(title="ET0 Prediction API", version="1.0")

# Define input schema using Pydantic

class WeatherInput(BaseModel):
    ta_max: float
    ta_min: float
    ta_mean: float
    rh_max: float
    rh_min: float
    rh_mean: float
    rs_mean: float
    wind_speed_10m: float

@app.get("/")
def home():
    return {"message": "ET0 Prediction API is running!"}

@app.post("/predict_cb/")
def predict_et0(
    ta_max: List[float] = Body(...),
    rh_mean: List[float] = Body(...),
    rs_mean: List[float] = Body(...)
):
    # print(ta_max)

    new_weather_data = pd.DataFrame({
    "ta_max": ta_max,       
    "rs_mean": rs_mean,       
    "rh_mean": rh_mean,  
    # "ta_min": rh_mean,       
    # "ta_mean": [26.4],
    # "rh_max": [75],         
    # "rh_min": [30],  
    # "wind_speed_10m": [2.5]
    })

    # Predict ET0
    predicted_et0 = model_data.predict(new_weather_data)
    print(predicted_et0.tolist())
    return {"predicted_et0": predicted_et0.tolist()}
