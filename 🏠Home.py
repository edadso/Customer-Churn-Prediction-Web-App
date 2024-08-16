import streamlit as st
import yaml
from yaml.loader import  SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import Hasher

# Set up Home page
st.set_page_config(page_title = "Customer Churn Prediction App",
                   page_icon = "📈",
                   layout = "wide")
st.markdown("<h1 style='color: lightblue;'> 📈 CUSTOMER CHURN PREDICTION APP</h1>", unsafe_allow_html=True)

# st.sidebar.markdown("""<img src = "https://th.bing.com/th/id/OIF.cHBXWEtI6X6PZcpwcf6VXg?rs=1&pid=ImgDetMain" width = "350" height = "250" />""", unsafe_allow_html = True)

st.markdown(
            """
            This application uses machine learning models to predict customer churn leveraging customer data
            """
            )

    # Create two columns
col1, col2 = st.columns(2)

with col1:   
    st.write("### Key Features")
    st.write(
                """
            - **Data**: Displays uploaded data.
            - **Predict**: Displays predictions for customer churn.
            - **Dashboard**: Explore interactive data visualizations for insghts.
            - **History**: Shows past predictions.
                """
                )
            
    st.write("### Machine Learning Integration")
    st.write(
                """
            - **Accurate Predictions**: Integrate advanced ML algorithms for accurate predictions.
            - **Variety**: Choose between two Machine Learning models.
                """
                )

with col2:
    st.write("### User Benefits")
    st.write(
                """
            - **Prediction**: Accurate predictions.
            - **Data-Driven Decisions**: Make informed decisions backed by data.
            - **Enhanced Insights**: Understand customer behavior.
            - **Real-Time Monitoring**: The app continuously monitors customer data and provides real-time updates.
                """
                )
            
with st.expander("**Need Help?**", expanded = False):
    st.write(
                """
                Refer to the [documentation](https://github.com/edadso/Customer-Churn-Prediction-Web-App) or [contact support](emmanueldadson36@gmail.com).
                """
                )

    st.write("#### About Developer")
    st.write(
                """
                A dedicated data and business analyst specializing in Data Analytics and Machine Learning,
                I leverage data-driven insights and advanced algorithms to tackle complex business challenges and shape strategic decisions.
                """
                )

with st.expander("**Developer's Portfolio**", expanded = False):
    st.write(
                """
                - **GitHub**: [Emmanuel Dadson](https://github.com/edadso)
                - **LinkedIn**: [Emmanuel Dadson](https://www.linkedin.com/in/emmanuel-dadson)
                - **Medium**: [Emmanuel Dadson](https://medium.com/@emmanueldadson36)
                - **Email**: emmanueldadson36@gmail.com
                """
                )

