import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import time
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

# Calculate the path you want to add
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Add it to sys.path only if it's not already there
if root_path not in sys.path:
    sys.path.append(root_path)

# Import custom modules
from utils import func

# Set up Home page
st.set_page_config(page_title = "Customer Churn Prediction App", page_icon = "🔭", layout="wide")
   

user_choice = st.sidebar.radio("### Select a page", options = ["Data Understanding", "Data Hub"], key = "option_selected")


if st.session_state["option_selected"] == "Data Understanding":
    st.info("## 📚 Data Understanding")
    st.markdown(
                    """
                The dataset for prediction contains various customer attributes that can help us understand and predict customer churn.
                Each column represents a different aspect of the customer's profile, service usage, and payment behavior.
                Note that these are the features the models were trained with.

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


if st.session_state["option_selected"] == "Data Hub":
    st.markdown("<h1 style='color: lightblue;'> 📚 Data Hub</h1>", unsafe_allow_html=True)
    st.info(f"### *Welcome To Data Hub*")
    st.markdown(f"#### **Uploaded data will be availbale for prediction in the predict page**") 

    with st.expander("## **Explore the dataset used for testing here**", expanded = False, icon = "👇"):
            df = func.load_data()
            
            # Display data preview
            st.data_editor(df)
                
            # Display data statistics
            left, right = st.columns(2)
            with left:
                 st.write(f"#### Data Statistics")
                 st.write(df.describe())
                 st.write(f"#### Data Shape")
                 st.write(df.shape)
                 st.write(f"#### Number of Duplicated Rows")
                 st.write(df.duplicated().sum())

            with right:            
                st.write(f"#### Missing Values")
                st.write(df.isnull().sum())
                st.write(f"#### Unique Values")
                st.write(df.nunique())
                

    with st.expander("**Upload your dataset here**", expanded = False, icon = "👇"):
            
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
                    data["SeniorCitizen"] = data["SeniorCitizen"].map({1: "Yes", 0: "No"})
                    data["tenure"] = pd.to_numeric(data["tenure"], errors = "coerce")
                    data["MonthlyCharges"] = pd.to_numeric(data["MonthlyCharges"], errors = "coerce")
                    data["TotalCharges"] = pd.to_numeric(data["TotalCharges"], errors = "coerce")

                    # Store the data in session_state
                    st.session_state["uploaded_data"] = data
                    
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

                # Option to explore data
                if st.checkbox("Explore data (Optional)"):
                    # Display data statistics
                    left, right = st.columns(2)
                    with left:
                        st.write(f"#### Data Statistics")
                        st.write(data.describe())
                        st.write(f"#### Data Shape")
                        st.write(data.shape)
                        st.write(f"#### Number of Duplicated Rows")
                        st.write(data.duplicated().sum())

                    with right:            
                        st.write(f"#### Missing Values")
                        st.write(data.isnull().sum())
                        st.write(f"#### Unique Values")
                        st.write(data.nunique())
                   
            else:
                st.info("Please upload a file to preview the data.")

         
# Load lottie
lottie_animation = func.load_lottie("assets/Animation_data.json")
with st.sidebar:
    st_lottie(lottie_animation, height = 350)

    
    
