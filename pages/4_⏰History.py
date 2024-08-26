import streamlit as st
import pandas as pd
import os


# Set up Home page
st.set_page_config(page_title = "Customer Churn Prediction App", page_icon = "🔭", layout = "wide")

st.markdown("<h1 style='color: lightblue;'> ⏰ Customer Churn Prediction History</h1>", unsafe_allow_html=True)


# History of Single predictions
@st.cache_data(persist = True)
def data_history():
    if os.path.exists("./data/history.csv"):
        history_df = pd.read_csv("./data/history.csv")
    else:
        history_df = pd.DataFrame()
    return history_df


# Prediction history on inbuilt data
@st.cache_data(persist = True)
def load_data():
    if os.path.exists("./data/inbuilt_data_history.csv"):
        data = pd.read_csv("./data/inbuilt_data_history.csv", index_col = "customerID")
    else:
        data = pd.DataFrame()
    return data


# Predictions history on uploaded data
@st.cache_data(persist = True)
def load_uploaded_data_history():
    if os.path.exists("./data/uploaded_data_history.csv"):
        uploaded_data_history_df = pd.read_csv("./data/uploaded_data_history.csv", index_col = "customerID")
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
            df = st.dataframe(data_history())
    
    elif user_choice == "Bulk Prediction (For test data)":
        st.info("### 🔓 Churn Status Unlocked")
        st.subheader("Bulk Prediction History (For Test Data)")
        if st.button("View History"):
            df = st.dataframe(load_data())
    
    elif user_choice == "Bulk Prediction (For uploaded data)":
        st.info("### 🔓 Churn Status Unlocked")
        st.subheader("Bulk Prediction History (For Uploaded Data)")
        if st.button("View History"):
            df = st.dataframe(load_uploaded_data_history())

    return df

# Execute function
view_prediction_history()

