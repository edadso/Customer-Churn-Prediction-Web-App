import streamlit as st
import pandas as pd
import numpy as np
import datetime
import joblib
import os

# Set up Home page
st.set_page_config(page_title = "Customer Churn Prediction App", page_icon = "📈", layout = "wide")

# Load gradient boost and threshold
@st.cache_resource(show_spinner = "Model Loading")
def load_gradient_boost():
    model, threshold = joblib.load("./models/gradient_boost_model.joblib")
    return model, threshold

# Load logistic regression and threshold
@st.cache_resource(show_spinner = "Data Loading")
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

    probability = pipeline.predict_proba(df)[:, 1]
    pred = (probability >= threshold).astype(int)
    pred = pred[0]
    prediction = encoder.inverse_transform(pred.reshape(-1))

    # Copy the original DataFrame to avoid modifying it directly
    history_df = df.copy()
    
    # Get the current date and time
    now = datetime.datetime.now()
    formatted_time = f"Time: {now.hour:02d}:{now.minute:02d} Date: {now.date()}"
    
    # Add relevant information to the DataFrame
    history_df["Prediction_Time"] = formatted_time
    history_df["Model_used"] = st.session_state["selected_model"]
    history_df["Customer_Churn_status"] = prediction
    history_df["Probability"] = np.round(probability*100, 2)

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
            tenure = st.number_input("Months of tenure", min_value = 1, max_value = 100, key = "tenure")
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


# def reset_session_state():
#     # Reset specific session state variables
#     st.session_state["prediction"] = None
#     st.session_state["probability"] = None
    
#     # Iterate over session state keys and delete all except specified ones
#     keys_to_keep = {"prediction", "probability", "selected_model"}
#     keys_to_delete = [key for key in st.session_state.keys() if key not in keys_to_keep]
    
#     for key in keys_to_delete:
#         del st.session_state[key]



if __name__ == "__main__":

    pipeline, encoder, threshold = select_model()

    if pipeline and encoder and threshold:
        entry_form(pipeline, encoder, threshold)

        probability = st.session_state["probability"]
        prediction = st.session_state["prediction"]

        if prediction == "Yes":
            st.markdown(f"#### ❌ Customer will churn.\nAt a probability of {probability[0]*100:.2f}%")
        elif prediction == "No":
            st.markdown(f"#### ✅ Customer will not churn.\nAt a probability of {probability[0]*100:.2f}%")
        else:
            st.markdown("#### No prediction made yet")
        
        # st.session_state









