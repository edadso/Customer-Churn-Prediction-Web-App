import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt

# Set up Home page
st.set_page_config(page_title = "Customer Churn Prediction App",
                   page_icon = "🔭",
                   layout="wide"
                   )

st.markdown("<h1 style='color: lightblue;'> 📊 Analytics Hub</h1>", unsafe_allow_html=True)

# Load data
@st.cache_data(persist = True)
def load_data():
    df = pd.read_csv("./data/data_output.csv")
    return df

df = load_data()

st.info("#### Exploratory Data Analysis")
# Create coulmns
left_column, midde_column, right_column = st.columns(3)
with left_column:
    # Create boxplot for MonthlyCharges
    fig, ax = plt.subplots()
    sns.set_style("dark")
    sns.boxplot(df.drop(["TotalCharges"], axis = 1), palette = "rocket")
    ax.set_title("Boxplot")
    st.pyplot(fig)

with midde_column:
    # Create boxplot for TotalCharges
    fig, ax = plt.subplots()
    sns.set_style("dark")
    sns.boxplot(df["TotalCharges"], palette = "rocket")
    ax.set_title("Boxplot of Total Charges")
    st.pyplot(fig)

with right_column:
    # Create create correlation heatmap
    fig, ax = plt.subplots()
    sns.set_style("dark")
    sns.heatmap(df[["TotalCharges", "MonthlyCharges", "tenure"]].dropna().corr(), annot=True, cmap="coolwarm", linewidths=0.5)
    ax.set_title("Correlation Matrix")
    st.pyplot(fig)

# Create pair plot
sns.set_style("dark")
pairplot = sns.pairplot(df[["Churn", "TotalCharges", "tenure", "MonthlyCharges"]], hue="Churn")
pairplot.fig.suptitle("Pairplot")
st.pyplot(pairplot)


left, middle, right = st.columns(3)
with left:
    # Create countplot for SeniorCitizen
    fig, ax = plt.subplots()
    sns.set_style("dark")
    sns.countplot(data = df, x = "SeniorCitizen", hue = "Churn", palette = "rocket")
    ax.set_title("Distribution of SeniorCitizen")
    st.pyplot(fig)

with middle:
    # Create countplot for InternetService
    fig, ax = plt.subplots()
    sns.set_style("dark")
    sns.countplot(data = df, x = "InternetService", hue = "Churn", palette = "rocket")
    ax.set_title("Distribution of InternetService")
    st.pyplot(fig)

with right:
    # Create countplot for Contract
    fig, ax = plt.subplots()
    sns.set_style("dark")
    sns.countplot(data = df, x = "Contract", hue = "Churn", palette = "rocket")
    ax.set_title("Distribution of Contract")
    st.pyplot(fig)




