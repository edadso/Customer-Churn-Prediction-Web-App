import streamlit as st
from streamlit_lottie import st_lottie
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
st.set_page_config(page_title = "Customer Churn Prediction App",
                   page_icon = "🔭",
                   layout = "wide")

st.markdown("<h1 style='color: lightblue;'> 🔭 CUSTOMER CHURN PREDICTION APP</h1>", unsafe_allow_html=True)

user_choice = st.sidebar.radio("Select a page", options = ["Wallpaper", "Home page"], key = "selected_page")

if st.session_state["selected_page"] == "Wallpaper":
    st.image("assets/customer_churn.png", width=900)


if st.session_state["selected_page"] == "Home page":
    st.markdown(
                """
                This application uses machine learning models to predict customer churn leveraging customer data
                """
                )

        # Create two columns
    col1, col2 = st.columns(2)

    with col1:   
        st.write("### 🧰 Key Features")
        st.write(
                    """
                - **Data**: Displays both inbuilt and uploaded datasets.
                - **Predict**: Displays customer churn status and prediction probability.
                - **Dashboard**: Shows interactive data visualizations for quick insghts.
                - **History**: Shows past predictions.
                    """
                    )
                
        st.write("### 👥 User Benefits")
        st.write(
                    """
                - **Prediction**: Accurate predictions.
                - **Data-Driven Decisions**: Make informed decisions backed by data.
                - **Enhanced Insights**: Understand customer behavior.
                - **Real-Time Monitoring**: The app continuously monitors customer data and provides real-time updates.
                - **Usability**: Provides a highly intuitive and user-friendly experience.
                    """
                    )
        
    with col2:
        st.write("### 🤖 Machine Learning Integration")
        st.markdown(
                    """
            - **Model Variety**: Select from two different Machine Learning models:
                1. **Gradient Boost Classifier**
                2. **Logistic Regression**
            - **Performance Metrics**: Compare the performance of both models:
                1. **Gradient Boost Classifier**
                    - `Prediction Accuracy: 81%`
                    - `AUC-ROC Score: 86%`
                    - `False Negative Rate: 5%`
                2. **Logistic Regression**
                    - `Prediction Accuracy: 80%`
                    - `AUC-ROC Score: 86%`
                    - `False Negative Rate: 7%`
                   """
                  )
                
    with st.expander("**Need Help?**", expanded = False):
        st.write(
                    """
                    Refer to the [documentation](https://github.com/edadso/Customer-Churn-Prediction-Web-App) or
                    
                    📧 emmanueldadson36@gmail.com.
                    """
                    )

        st.write("#### 👨‍💻 About Developer")
        st.write(
                    """
                    A dedicated data and business analyst specializing in Data Analytics and Machine Learning,
                    I leverage data-driven insights and advanced algorithms to tackle complex business challenges and shape strategic decisions.
                    """
                    )

    with st.expander("**Developer's Portfolio**", expanded = False):
        st.markdown(
                    """
            - <img src='https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/github.svg' alt='GitHub' height='20' style='filter: invert(100%) sepia(0%) saturate(0%) hue-rotate(0deg) brightness(100%) contrast(100%); margin-right: 8px;'> [GitHub](https://github.com/edadso)
            - <img src='https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/linkedin.svg' alt='LinkedIn' height='20' style='filter: invert(100%) sepia(0%) saturate(0%) hue-rotate(0deg) brightness(100%) contrast(100%); margin-right: 8px;'> [LinkedIn](https://www.linkedin.com/in/emmanuel-dadson)
            - <img src='https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/medium.svg' alt='Medium' height='20' style='filter: invert(100%) sepia(0%) saturate(0%) hue-rotate(0deg) brightness(100%) contrast(100%); margin-right: 8px;'> [Medium](https://medium.com/@emmanueldadson36)
            - <img src='https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/gmail.svg' alt='Email' height='20' style='filter: invert(100%) sepia(0%) saturate(0%) hue-rotate(0deg) brightness(100%) contrast(100%); margin-right: 8px;'> emmanueldadson36@gmail.com
                    """,
                    unsafe_allow_html=True
                    )
        

# Load lottie
lottie_animation = func.load_lottie("assets/Animation.json")
with st.sidebar:
    st_lottie(lottie_animation, height = 350)

