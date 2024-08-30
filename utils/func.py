import streamlit as st
import pandas as pd
import json
from streamlit_lottie import st_lottie

# Create function to load Telco-churn-last-2000
@st.cache_data(persist = True)
def load_data():
    """
    loads Telco-churn-last-2000 to the script
    """
    df = pd.read_excel("./data/Telco-churn-last-2000.xlsx")
    df["SeniorCitizen"] = df["SeniorCitizen"].map({1: "Yes", 0: "No"})
    df["tenure"] = pd.to_numeric(df["tenure"], errors = "coerce")
    df["MonthlyCharges"] = pd.to_numeric(df["MonthlyCharges"], errors = "coerce")
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors = "coerce")
    return df


# Function to load lottie files
def load_lottie(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
