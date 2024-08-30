import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import json
import os
import sys

# Calculate the path you want to add
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add it to sys.path only if it's not already there
if root_path not in sys.path:
    sys.path.append(root_path)

# Import custom modules
from utils import func


# Set up Home page
st.set_page_config(page_title = "Customer Churn Prediction App", page_icon = "🔭", layout = "wide")

st.markdown("<h1 style='color: lightblue;'> ⏰ Customer Churn Prediction History</h1>", unsafe_allow_html=True)


# History of Single predictions
def data_history():
    if os.path.exists("./data/history.csv"):
        history_df = pd.read_csv("./data/history.csv")
    else:
        history_df = pd.DataFrame()
    return history_df


# Prediction history on inbuilt data
def load_data():
    if os.path.exists("./data/inbuilt_data_history.csv"):
        data = pd.read_csv("./data/inbuilt_data_history.csv")
    else:
        data = pd.DataFrame()
    return data


# Predictions history on uploaded data
def load_uploaded_data_history():
    if os.path.exists("./data/uploaded_data_history.csv"):
        uploaded_data_history_df = pd.read_csv("./data/uploaded_data_history.csv")
    else:
        uploaded_data_history_df = pd.DataFrame()
    return uploaded_data_history_df
    

# Function to view prediction history based on user's choice
def view_prediction_history():
    user_choice = st.sidebar.radio("### Display Prediction History",
                                   options = ["Single Prediction", "Bulk Prediction (For test data)", "Bulk Prediction (For uploaded data)"],
                                   key = "user_choice")
    df = None
    
    # Display the chosen data history
    if user_choice == "Single Prediction":
        st.info("### 🔓 Churn Status Unlocked")
        st.subheader("Single Prediction History")
        if st.button("View History"):
            df = st.dataframe(data_history().iloc[::-1])
    
    elif user_choice == "Bulk Prediction (For test data)":
        st.info("### 🔓 Churn Status Unlocked")
        st.subheader("Bulk Prediction History (For Test Data)")
        if st.button("View History"):
            df = st.dataframe(load_data())
    
    elif user_choice == "Bulk Prediction (For uploaded data)":
        st.info("### 🔓 Churn Status Unlocked")
        st.subheader("Bulk Prediction History (For Uploaded Data)")
        if st.button("View History"):
            # Load the historical data
            df = load_uploaded_data_history()

            if df is not None:
                # Display data in streamlit
                st.dataframe(df)
                # Save df to session state
                st.session_state["dashboard_data"] = df

    return df

# Execute function
view_prediction_history()


# Load lottie
lottie_animation = func.load_lottie("assets/Animation_history.json")
with st.sidebar:
    st_lottie(lottie_animation, height = 350)