import streamlit as st
# import pyodbc
import os
import pandas as pd
import streamlit_authenticator as stauth
# import pymssql
import time
import yaml
from yaml.loader import  SafeLoader
from streamlit_authenticator.utilities import Hasher

# Set up Home page
st.set_page_config(page_title = "Customer Churn Prediction App",
                   page_icon = "📚",
                   layout="wide"
                   )
   
# Load yaml file    
with open("config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
Hasher.hash_passwords(config['credentials'])

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
    st.sidebar.warning("Please enter username and password")
    st.sidebar.code(
            """
            Test Account's Credentials:
            Username: test_user
            Password: user123
            """
            )
    st.info("## 📚 Data Understanding")
    st.markdown(
                """
            The dataset for prediction contains various customer attributes that can help us understand and predict customer churn.
            Each column represents a different aspect of the customer's profile, service usage, and payment behavior.
            The columns in our dataset are:
            #### Feature Description:
                """
                )

    # Create columns
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
                    """
        - **customerID**: Unique identifier for each customer.
        - **gender**: Customer's gender.
        - **SeniorCitizen**: Indicates if the customer is a senior citizen (Yes) or not (No).
        - **Partner**: Indicates if the customer has a partner.
        - **Dependents**: Indicates if the customer has dependents.
        - **tenure**: Number of months the customer has stayed with the company.
        - **PhoneService**: Indicates if the customer has a phone service.
        - **MultipleLines**: Indicates if the customer has multiple phone lines.
        - **InternetService**: Type of internet service the customer has (e.g., DSL, Fiber optic, None).
        - **OnlineSecurity**: Indicates if the customer has online security add-on.
        - **OnlineBackup**: Indicates if the customer has online backup add-on.
                    """
                    )

    with col2:
        st.markdown(
                    """
        - **DeviceProtection**: Indicates if the customer has device protection add-on.
        - **TechSupport**: Indicates if the customer has tech support add-on.
        - **StreamingTV**: Indicates if the customer has streaming TV service.
        - **StreamingMovies**: Indicates if the customer has streaming movies service.
        - **Contract**: Type of contract the customer has (e.g., month-to-month, one year, two years).
        - **PaperlessBilling**: Indicates if the customer uses paperless billing.
        - **PaymentMethod**: Method of payment used by the customer (e.g., electronic check, mailed check, bank transfer, credit card).
        - **MonthlyCharges**: The amount charged to the customer monthly.
        - **TotalCharges**: The total amount charged to the customer.
        - **Churn**: Indicates if the customer has churned (Yes) or not (No)
                    """
                    )
    
if st.session_state["authentication_status"] is None:
    st.sidebar.warning("Please enter username and password")
    st.sidebar.code(
            """
            Test Account's Credentials:
            Username: test_user
            Password: user123
            """
            )
    st.info("## 📚 Data Understanding")
    st.markdown(
                """
            The dataset for prediction contains various customer attributes that can help us understand and predict customer churn.
            Each column represents a different aspect of the customer's profile, service usage, and payment behavior.
            The columns in our dataset are:
            #### Feature Description:
                """
                )

    # Create columns
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
                    """
        - **customerID**: Unique identifier for each customer.
        - **gender**: Customer's gender.
        - **SeniorCitizen**: Indicates if the customer is a senior citizen (Yes) or not (No).
        - **Partner**: Indicates if the customer has a partner.
        - **Dependents**: Indicates if the customer has dependents.
        - **tenure**: Number of months the customer has stayed with the company.
        - **PhoneService**: Indicates if the customer has a phone service.
        - **MultipleLines**: Indicates if the customer has multiple phone lines.
        - **InternetService**: Type of internet service the customer has (e.g., DSL, Fiber optic, None).
        - **OnlineSecurity**: Indicates if the customer has online security add-on.
        - **OnlineBackup**: Indicates if the customer has online backup add-on.
                    """
                    )

    with col2:
        st.markdown(
                    """
        - **DeviceProtection**: Indicates if the customer has device protection add-on.
        - **TechSupport**: Indicates if the customer has tech support add-on.
        - **StreamingTV**: Indicates if the customer has streaming TV service.
        - **StreamingMovies**: Indicates if the customer has streaming movies service.
        - **Contract**: Type of contract the customer has (e.g., month-to-month, one year, two years).
        - **PaperlessBilling**: Indicates if the customer uses paperless billing.
        - **PaymentMethod**: Method of payment used by the customer (e.g., electronic check, mailed check, bank transfer, credit card).
        - **MonthlyCharges**: The amount charged to the customer monthly.
        - **TotalCharges**: The total amount charged to the customer.
        - **Churn**: Indicates if the customer has churned (Yes) or not (No)
                    """
                    )
      
elif st.session_state["authentication_status"]:
    authenticator.logout(location = "sidebar")
    st.info(f"### Welcome *{st.session_state['name']}*")

    # Upload file
    upload_file = st.file_uploader(label="Choose a file", type=["csv", "xlsx"])

    # Initialize session state variable for tracking data load status
    if "data_loaded" not in st.session_state:
        st.session_state.data_loaded = False

    if upload_file is not None:
        # Check for file type and read file
        try:
            if upload_file.name.endswith(".csv"):
                data = pd.read_csv(upload_file)
            elif upload_file.name.endswith(".xlsx"):
                data = pd.read_excel(upload_file)
            else:
                st.error("Unsupported file type!")
                data = None
        except Exception as e:
            st.error(f"Error reading this file: {str(e)}")
            data = None
        
        # Coerce non-numeric entries in numeric columns
        if data is not None:
            for col in data.select_dtypes(include=["number"]).columns:
                data[col] = pd.to_numeric(data[col], errors='coerce')

        # Display success message
        if data is not None and not st.session_state.data_loaded:
            success_msg = st.empty()
            success_msg.success("Data uploaded successfully!")
            # Display success message for 2 seconds
            time.sleep(2)
            # Clear success message
            success_msg.empty()
            st.session_state.data_loaded = True

        if data is not None:
            # Preview data
            st.subheader("Data Preview")
            st.write("First few rows of your data:")
            st.dataframe(data.head())

            # Option to display entire data
            if st.checkbox("Show entire data (Optional)"):
                st.dataframe(data)

    else:
        st.info("Please upload a file to preview the data.")
