# Customer-Churn-Prediction-Web-App
This project delivers customer churn prediction models through a user-friendly web application built with Streamlit. Tailored for third-party stakeholders with limited technical knowledge, the app offers an accessible and interactive solution for predicting and analyzing customer churn, eliminating the need to work with complex Jupyter notebooks.


## Table of Contents
- [Features](#features)
- [Usage](#usage)
- [Contributing](#contributing)
- [Author](#author)

## Features
### 1. Home Page
- **Overview:** Introduces the application and its purpose.
- **Key Elements:**
    - Provides an overview of the application.
    - Includes background information about the developer.

<img src="assets/home_page.jpg" alt="Home Page" width="850"/>

[Back to Table of Contents](#table-of-contents)


### 2. Data Page
- **Overview:** Offers insights into the data used for predictions and details customer attributes required for accurate predictions.
- **Key Features:**
    - Displays `built-in data` sourced from a GitHub repository, used for development and testing.
    - Allows users to upload their own data for analysis.
    - Provides comprehensive information about the data.
    - Ensures seamless integration of uploaded data into the prediction process on the Predict Page.

<img src="assets/data_page1.jpg" alt="Data Page" width="850"/>
<img src="assets/data_page2.jpg" alt="Data Page" width="850"/>

[Back to Table of Contents](#table-of-contents)

### 3. Predict Page
- **Overview:** Enables customer churn predictions, showing both churn status and prediction probability.
- **Key Features:**
    - Serves as a login gateway for users to perform `bulk predictions` after authentication.
    - Allows individual customer details to be entered for `single predictions` without requiring authentication.
    - Supports predictions using either built-in data or previously uploaded data.
    - Provides the option to choose between existing uploaded data or new data for predictions.
    - Utilizes the following models for predictions:
        1. **Gradient Boost Classifier:** Employed for both single and bulk predictions as the top-performing model.
        2. **Logistic Regression:** Used exclusively for single predictions.

<img src="assets/predict_page1.jpg" alt="Predict Page" width="850"/>
<img src="assets/predict_page2.jpg" alt="Predict Page" width="850"/>

[Back to Table of Contents](#table-of-contents)

### 4. History Page
- **Overview:** Provides a record of all predictions made by the user.
- **Key Features:**
    - Provides a detailed record of all user predictions for reference and analysis.
    - Individual predictions are added to the top of the history.
    - Bulk predictions replace existing entries to facilitate dashboard analysis.
 
<img src="assets/history_page.jpg" alt="History Page" width="850"/>

[Back to Table of Contents](#table-of-contents)

### 5. Dashboard
- **Overview:** Displays interactive visualizations for quick insights.
- **Key Features:**
    - **Exploratory Data Analysis (EDA) Dashboard:** Provides comprehensive visualizations and analyses of the data.
    - **Key Indicator Dashboard:** Showcases critical metrics through interactive visualizations.
    - Allows users to toggle between `built-in data` and `prediction history data` for display on the dashboard.

<img src="assets/dashboard_page1.jpg" alt="Dashboard" width="850"/>
<img src="assets/dashboard_page2.jpg" alt="Dashboard" width="850"/>

[Back to Table of Contents](#table-of-contents)

## Usage
1. **Launch the Application:** Initiate the application using Streamlit.
2. **Select a Dataset:** Choose from built-in datasets or upload your own data.
3. **Make Predictions:** Perform either single or bulk predictions.
4. **Review Prediction History:** Access and navigate through the prediction history.
5. **Explore Results:** Analyze the results and visualizations on the interactive dashboard.

[Back to Table of Contents](#table-of-contents)

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request.<br>For major changes, please open an issue first to discuss what you would like to change.

[Back to Table of Contents](#table-of-contents)

## Author

- <img src='https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/github.svg' alt='GitHub' height='20' style='filter: invert(100%) sepia(0%) saturate(0%) hue-rotate(0deg) brightness(100%) contrast(100%); margin-right: 8px;'> [GitHub](https://github.com/edadso)
- <img src='https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/linkedin.svg' alt='LinkedIn' height='20' style='filter: invert(100%) sepia(0%) saturate(0%) hue-rotate(0deg) brightness(100%) contrast(100%); margin-right: 8px;'> [LinkedIn](https://www.linkedin.com/in/emmanuel-dadson)
- <img src='https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/medium.svg' alt='Medium' height='20' style='filter: invert(100%) sepia(0%) saturate(0%) hue-rotate(0deg) brightness(100%) contrast(100%); margin-right: 8px;'> [Medium](https://medium.com/@emmanueldadson36)
- <img src='https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/gmail.svg' alt='Email' height='20' style='filter: invert(100%) sepia(0%) saturate(0%) hue-rotate(0deg) brightness(100%) contrast(100%); margin-right: 8px;'> emmanueldadson36@gmail.com            

[Back to Table of Contents](#table-of-contents)








