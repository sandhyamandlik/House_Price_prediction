import streamlit as st
import pandas as pd
import joblib

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="House Price Prediction", layout="wide")

# ---------------- CLEAN MODERN CSS ----------------
st.markdown("""
<style>
/* Main Background */
.stApp {
    background-color: #0f172a;
    color: white;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #020617;
}

/* Title */
h1 {
    color: #38bdf8;
    text-align: center;
}

/* Inputs */
label {
    font-weight: 500;
}

/* Button */
.stButton>button {
    background-color: #22c55e;
    color: white;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: 600;
    border: none;
}

.stButton>button:hover {
    background-color: #16a34a;
}

/* Metric color */
[data-testid="stMetricValue"] {
    color: #38bdf8;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
model = joblib.load("model.pkl")
pipeline = joblib.load("pipeline.pkl")

# ---------------- SIDEBAR ----------------
st.sidebar.title("📊 Model Info")

st.sidebar.metric("Accuracy (R² Score)", "0.85")
st.sidebar.caption("Random Forest Model")

st.sidebar.markdown("---")

# ---------------- MAIN UI ----------------
st.title("🏠 House Price Prediction")

# ----------- INPUTS -------------
col1, col2 = st.columns(2)

with col1:
    longitude = st.number_input("Longitude", value=-122.23)
    latitude = st.number_input("Latitude", value=37.88)
    housing_median_age = st.number_input("Median Age", value=41)
    total_rooms = st.number_input("Total Rooms", value=880)

with col2:
    total_bedrooms = st.number_input("Bedrooms", value=129)
    population = st.number_input("Population", value=322)
    households = st.number_input("Households", value=126)
    median_income = st.number_input("Income", value=8.3252)

ocean_proximity = st.selectbox(
    "Ocean Proximity",
    ["<1H OCEAN", "INLAND", "ISLAND", "NEAR BAY", "NEAR OCEAN"]
)

# ----------- Currency -------------
currency = st.radio(
    "Currency",
    ["USD ($)", "INR (₹)"],
    horizontal=True
)

st.markdown("---")

# ----------- Prediction -------------
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

    price = prediction[0]

    # Currency Conversion
    if currency == "INR (₹)":
        price *= 83
        symbol = "₹"
        price_str = f"{price:,.0f}".replace(",", " ")
    else:
        symbol = "$"
        price_str = f"{price:,.0f}"

    # Result Card UI
    st.markdown(f"""
    <div style='
        background: linear-gradient(135deg, #1e293b, #334155);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin-top: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    '>
        <h2 style="color:#94a3b8;">Predicted Price</h2>
        <h1 style="color:#22c55e; font-size:40px;">{symbol}{price_str}</h1>
    </div>
    """, unsafe_allow_html=True)