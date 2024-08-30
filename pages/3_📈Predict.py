import streamlit as st
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import Hasher
from streamlit_lottie import st_lottie
from yaml.loader import  SafeLoader
import pandas as pd
import numpy as np
import datetime
import joblib
import yaml
import json
import sys
import os


# Calculate the path you want to add
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add it to sys.path only if it's not already there
if root_path not in sys.path:
    sys.path.append(root_path)

# Import custom modules
from utils import func

# Set up Home page
st.set_page_config(page_title = "Customer Churn Prediction App", page_icon = "🔭", layout = "wide")

# Load yaml file    
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
Hasher.hash_passwords(config["credentials"])

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["pre-authorized"],
    False
)

authenticator.login("sidebar", "Login")

if st.session_state["authentication_status"] is False:
    st.sidebar.error("Incorrect Username/Password")
    st.sidebar.info("Please enter username and password to access the bulk prediction page")
    st.sidebar.code(
            """
            Test Account's Credentials:
            Username: test_user
            Password: user123
            """
            )
      
if st.session_state["authentication_status"] is None:
    st.sidebar.info("Please enter username and password to access the bulk prediction page")
    st.sidebar.code(
            """
            Test Account's Credentials:
            Username: test_user
            Password: user123
            """
            )

    # Load gradient boost and threshold
    @st.cache_resource(show_spinner = "Model Loading")
    def load_gradient_boost():
        model, threshold = joblib.load("./models/gradient_boost_model.joblib")
        return model, threshold

    # Load logistic regression and threshold
    @st.cache_resource(show_spinner = "Model Loading")
    def load_logistic_regression():
        model, threshold = joblib.load("./models/logistic_regression_model.joblib")
        return model, threshold


    def select_model():
        col1, col2 = st.columns(2)

        with col1:
            st.selectbox("Select a model", options = ["Gradient Boost", "Logistic Regression"], key = "selected_model")
        with col2:
            pass

        if st.session_state["selected_model"] == "Gradient Boost":
            pipeline, threshold = load_gradient_boost()
        else:
            pipeline, threshold = load_logistic_regression()

        if pipeline and threshold:
            encoder = joblib.load("./models/encoder.joblib")
        else:
            encoder = None

        return pipeline, encoder, threshold


    if "probability" not in st.session_state:
        st.session_state["probability"] = None
    if "prediction" not in st.session_state:
        st.session_state["prediction"] = None


    def make_prediction(pipeline, encoder, threshold):
        data = [[st.session_state["gender"], st.session_state["SeniorCitizen"], st.session_state["Partner"], st.session_state["Dependents"],
                st.session_state["tenure"], st.session_state["PhoneService"], st.session_state["MultipleLines"],
                st.session_state["InternetService"], st.session_state["OnlineSecurity"], st.session_state["OnlineBackup"],
                st.session_state["DeviceProtection"], st.session_state["TechSupport"], st.session_state["StreamingTV"],
                st.session_state["StreamingMovies"], st.session_state["Contract"], st.session_state["PaperlessBilling"],
                st.session_state["PaymentMethod"], st.session_state["MonthlyCharges"], st.session_state["TotalCharges"]]]
        
        columns = ["gender", "SeniorCitizen", "Partner", "Dependents", "tenure", "PhoneService", "MultipleLines",
                "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
                "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod", "MonthlyCharges", "TotalCharges"]
        
        df = pd.DataFrame(data, columns = columns)

        probability = pipeline.predict_proba(df)
        pred = (probability[:, 1] >= threshold).astype(int)
        pred = int(pred[0])
        prediction = encoder.inverse_transform([pred])[0]

        # Copy the original DataFrame to avoid modifying it directly
        history_df = df.copy()
        
        # Get the current date and time
        now = datetime.datetime.now()
        formatted_time = f"{now.hour:02d}:{now.minute:02d}"
        formatted_date = f"{now.date()}"
        
        # Add relevant information to the DataFrame
        history_df.insert(0, "Prediction_Date", formatted_date)
        history_df.insert(1, "Prediction_Time", formatted_time)
        history_df["Model_used"] = st.session_state["selected_model"]
        history_df["Customer_Churn_status"] = prediction
        history_df["Probability"] = np.where(pred == 0, np.round(probability[:, 0]*100, 2), np.round(probability[:, 1]*100, 2))
        
        # Save the DataFrame to a CSV file, appending to it if it already exists
        history_df.to_csv("./data/history.csv", mode = "a", header = not os.path.exists("./data/history.csv"), index = False)

        st.session_state["probability"] = probability
        st.session_state["prediction"] = prediction

        return probability, prediction


    def entry_form(pipeline, encoder, threshold):
        st.markdown("#### Enter Customer's Information")
        with st.form(key = "Customer_info"):

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                gender = st.selectbox("Gender", options = ["Male", "Female"], key = "gender")
                SeniorCitizen = st.selectbox("Senior Citizen", options = ["Yes", "No"], key = "SeniorCitizen")
                Dependents = st.selectbox("Has dependents", options = ["Yes", "No"], key = "Dependents")
                Partner = st.selectbox("Has a partner", options = ["Yes", "No"], key = "Partner")
                PhoneService = st.selectbox("Has phone service", options = ["Yes", "No"], key = "PhoneService")
                            
            with col2:
                DeviceProtection = st.selectbox("Has device protection",options = ["Yes", "No", "No internet service"], key = "DeviceProtection")
                OnlineBackup = st.selectbox("Has online backup", options = ["Yes", "No", "No internet service"], key = "OnlineBackup")
                OnlineSecurity = st.selectbox("Has online security", options = ["Yes", "No", "No internet service"], key = "OnlineSecurity")
                TechSupport = st.selectbox("Has tech support", options = ["Yes", "No", "No internet service"], key = "TechSupport")
                InternetService = st.selectbox("Internet service", options = ["DSL", "Fiber optic", "No"], key = "InternetService")
                
            with col3:
                MultipleLines = st.selectbox("Multiple lines", options = ["Yes", "No", "No phone service"], key = "MultipleLines")
                PaperlessBilling = st.selectbox("Paperless billing", options = ["Yes", "No"], key = "PaperlessBilling")
                StreamingTV = st.selectbox("Streaming TV", options = ["Yes", "No", "No internet service"], key = "StreamingTV")
                PaymentMethod = st.selectbox("Payment method", options = ["Electronic check", "Mailed check", "Bank transfer", "Credit card"], key = "PaymentMethod")
                StreamingMovies = st.selectbox("Streaming movies", options = ["Yes", "No", "No internet service"], key = "StreamingMovies")      
                        
            with col4:
                Contract = st.selectbox("Contract type", options = ["Month-to-month", "One year", "Two year"], key = "Contract")
                tenure = st.number_input("Number of Months (tenure)", min_value = 1, key = "tenure")
                MonthlyCharges = st.number_input("Monthly charges ($)", min_value = 0.0, step = 0.01, key = "MonthlyCharges")
                TotalCharges = st.number_input("Total charges ($)", min_value = 0.0, step = 0.01, key = "TotalCharges")

            sumbit_button = st.form_submit_button("Make Prediction")

            if sumbit_button:
                if None in [gender, SeniorCitizen, Dependents, Partner, tenure, PhoneService, PaymentMethod,
                            DeviceProtection, OnlineBackup, OnlineSecurity, TechSupport, MonthlyCharges, InternetService,
                            MultipleLines, PaperlessBilling, StreamingTV, StreamingMovies, Contract, TotalCharges]:
                    st.warning("Please fill in all required fields.")
                else:
                    make_prediction(pipeline, encoder, threshold)


    if __name__ == "__main__":
        st.markdown("<h1 style='color: lightblue;'> 🔮 Prediction Hub</h1>", unsafe_allow_html=True)

        pipeline, encoder, threshold = select_model()

        if pipeline and encoder and threshold:
            entry_form(pipeline, encoder, threshold)

            probability = st.session_state["probability"]
            prediction = st.session_state["prediction"]

            if prediction == "Yes":
                st.warning(f"#### ❌ Customer will churn.\nAt a probability of {probability[0][1]*100:.2f}%")
            elif prediction == "No":
                st.success(f"#### ✅ Customer will not churn.\nAt a probability of {probability[0][0]*100:.2f}%")
            else:
                st.markdown("#### No prediction made yet") 

     
elif st.session_state["authentication_status"]:
    authenticator.logout(location = "sidebar")
    st.markdown("<h1 style='color: lightblue;'> 📁 Bulk Prediction Hub</h1>", unsafe_allow_html=True)
    st.info(f"### You are in *{st.session_state['name']}* 😊")

    # Load gradient boost and threshold
    def load_gradient_boost():
        model, threshold = joblib.load("./models/gradient_boost_model.joblib")
        return model, threshold
    
    encoder = joblib.load("./models/encoder.joblib")

    def bulk_prediction(model, threshold, df, encoder):
        # Make predictions
        prob_score = model.predict_proba(df.drop(columns=["customerID"]))
        bulk_pred = (prob_score[:, 1] >= threshold).astype(int)
        # Inverse transform encoded predictions
        bulk_prediction = encoder.inverse_transform(bulk_pred)
        return bulk_prediction, prob_score

    def make_prediction(df, is_uploaded_data):
        
        # Define expected feature columns
        expected_features = ["gender", "SeniorCitizen", "Partner", "Dependents", "tenure", "PhoneService", "MultipleLines",
                             "InternetService", "OnlineSecurity", "OnlineBackup", "DeviceProtection", "TechSupport", "StreamingTV",
                             "StreamingMovies", "Contract", "PaperlessBilling", "PaymentMethod", "MonthlyCharges", "TotalCharges"]
        
        # Button to preview data
        if df is not None:
            # Load data
            if st.button("Preview Data"):
                st.dataframe(df.head())

            # Button to make prediction
            if st.button("Make Prediction"):
                # Check if uploaded data has same feature as expected
                if all(feature in df.columns for feature in expected_features):
                    model, threshold = load_gradient_boost()

                    if model is not None:
                        bulk_predict, probability_score = bulk_prediction(model, threshold, df, encoder)
            
                        # Copy the original DataFrame to avoid modifying it directly
                        bulk_history_df = df.copy()
                        
                        # Get the current date and time
                        now = datetime.datetime.now()
                        formatted_date = f"{now.date()}"
                        
                        # Add relevant information to the DataFrame
                        bulk_history_df.insert(1, "Prediction_Date", formatted_date)
                        bulk_history_df["Model_used"] = "Gradient Boost Classifier"
                        bulk_history_df["Churn"] = bulk_predict
                        bulk_history_df["Probability"] = np.where(bulk_predict == 0, np.round(probability_score[:, 0]*100, 2), np.round(probability_score[:, 1]*100, 2))

                        # Determine history file based on dataset source
                        history_file = "./data/uploaded_data_history.csv" if is_uploaded_data else "./data/inbuilt_data_history.csv"
                        
                        # Save the DataFrame to a CSV file, overrriding already existed file
                        bulk_history_df.to_csv(history_file, mode = "w", header = True, index = False)

                        st.success(f"#### Predictions made successfully.")
                    else:
                        st.error("### Failed to load Gradient Boost model.")
                else:
                    st.error("### Uploaded data does not match expected features.")

            # Button to preview prediction history
            if st.button("Preview Prediction"):
                history_file = "./data/uploaded_data_history.csv" if is_uploaded_data else "./data/inbuilt_data_history.csv"
                if os.path.exists(history_file):
                    history_df = pd.read_csv(history_file)
                    st.dataframe(history_df.head())
                else:
                    st.warning("### No prediction history found")


    def main():
        # Option to use inbuilt or uploaded data
        data_source = st.radio("Choose a data source", ["Inbuilt Data", "Use previously uploaded data", "Upload new data"])

        if data_source == "Inbuilt Data":

            df = func.load_data()

            # Load lottie
            lottie_animation = func.load_lottie("assets/Animation_predict.json")
            with st.sidebar:
                st_lottie(lottie_animation, height = 350)

            make_prediction(df, is_uploaded_data = False)

        elif data_source == "Use previously uploaded data":
            if "uploaded_data" in st.session_state:
                df = st.session_state["uploaded_data"]
                st.sidebar.success("### Using previously uploaded data from data page")

                if make_prediction(df, is_uploaded_data = True):
                    # Delete uploaded data from session state after successful prediction
                    st.session_state["uploaded_data"] = None

            lottie_animation = func.load_lottie("assets/Animation_predict.json")
            with st.sidebar:
                st_lottie(lottie_animation, height = 350)

        elif data_source == "Upload new data":
                
                # Upload data
                uploaded_file = st.sidebar.file_uploader("Upload Dataset", type = ["csv", "xlsx"])

                if uploaded_file is not None:
                    if uploaded_file.name.endswith(".csv"):
                        df = pd.read_csv(uploaded_file)
                    elif uploaded_file.name.endswith(".xlsx"):
                        df = pd.read_excel(uploaded_file)
                    else:
                        st.warning("Unsupported file type. Please upload a csv or xlsx file")
                    
                    # Coerce non-numeric entries in numeric columns to NaN
                    df["SeniorCitizen"] = df["SeniorCitizen"].map({1: "Yes", 0: "No"})
                    df["tenure"] = pd.to_numeric(df["tenure"], errors = "coerce")
                    df["MonthlyCharges"] = pd.to_numeric(df["MonthlyCharges"], errors = "coerce")
                    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors = "coerce")

                    make_prediction(df, is_uploaded_data = True)
                    
                else:
                    st.sidebar.warning("### Please upload a dataset and continue.")
        

                right, middle, left = st.columns([2, 2, 1])
                with left:
                    # Load lottie
                    lottie_animation = func.load_lottie("assets/Animation_predict.json")
                    # with st.sidebar:
                    st_lottie(lottie_animation, height = 350)

    main()

    
   









