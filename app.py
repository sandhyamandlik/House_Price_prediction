import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load trained model and pipeline
model = joblib.load("model.pkl")
pipeline = joblib.load("pipeline.pkl")

st.set_page_config(page_title="House Price Prediction", layout="centered")

st.title("🏠 House Price Prediction App")
st.write("Enter house details to predict the median house value")

# ----------- User Inputs -------------
longitude = st.number_input("Longitude", value=-122.23)
latitude = st.number_input("Latitude", value=37.88)
housing_median_age = st.number_input("Housing Median Age", value=41)
total_rooms = st.number_input("Total Rooms", value=880)
total_bedrooms = st.number_input("Total Bedrooms", value=129)
population = st.number_input("Population", value=322)
households = st.number_input("Households", value=126)
median_income = st.number_input("Median Income", value=8.3252)

ocean_proximity = st.selectbox(
    "Ocean Proximity",
    ["<1H OCEAN", "INLAND", "ISLAND", "NEAR BAY", "NEAR OCEAN"]
)

# ----------- Predict Button -------------
if st.button("Predict Price"):
    input_data = pd.DataFrame([{
        "longitude": longitude,
        "latitude": latitude,
        "housing_median_age": housing_median_age,
        "total_rooms": total_rooms,
        "total_bedrooms": total_bedrooms,
        "population": population,
        "households": households,
        "median_income": median_income,
        "ocean_proximity": ocean_proximity
    }])

    transformed_data = pipeline.transform(input_data)
    prediction = model.predict(transformed_data)

    st.success(f"🏡 Predicted House Price: ${prediction[0]:,.2f}")
