import streamlit as st
import os
import time
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Set up Home page
st.set_page_config(page_title = "Customer Churn Prediction App",
                   page_icon = "🔭",
                   layout="wide"
                   )


# Radio buttons to select between prediction history data or inbuilt data
data_source_choice = st.sidebar.radio("Choose Data Source", options = ["Inbuilt Data", "Prediction History"])

user_choice = st.sidebar.radio("Display a Dashboard", options = ["EDA Dashboard", "Analytical Dashboard"], key = "selected_dashboard")

# @st.cache_data(persist = True)
def load_inbuilt_data():
    if os.path.exists("./data/data_output.csv"):
        return pd.read_csv("./data/data_output.csv")
    else:
        st.error("Data file not found.")
        return None


# Load data based on user's choice
if data_source_choice == "Inbuilt Data":
    df = load_inbuilt_data()

elif data_source_choice == "Prediction History":
    if "dashboard_data" in st.session_state:
        df = st.session_state["dashboard_data"]

    else:
        st.error("No prediction history found.")
        df = None

# Now use the `df` for dashboard based on user’s selected dashboard
if df is not None and not df.empty:
    if st.session_state["selected_dashboard"] == "EDA Dashboard":
        left, middle, right = st.columns([1, 5, 1])
        with middle:
            st.markdown("<h1 style='color: lightblue;'> 🔍 Exploratory Data Analysis</h1>", unsafe_allow_html=True)

        st.write(df.head())


        # Left, Middle, Right Columns
        left_column, middle_column, right_column = st.columns(3)

        # Boxplot for MonthlyCharges
        with left_column:
            fig = px.box(df, y="MonthlyCharges", title="Boxplot of Monthly Charges", color_discrete_sequence=["#C70039"])
            st.plotly_chart(fig)

        # Boxplot for TotalCharges
        with middle_column:
            fig = px.box(df, y="TotalCharges", title="Boxplot of Total Charges", color_discrete_sequence=["#900C3F"])
            st.plotly_chart(fig)

        # Correlation Heatmap with Annotations and No Color Bar
        with right_column:
            corr_matrix = df[["TotalCharges", "MonthlyCharges", "tenure"]].dropna().corr()

            # Annotate the heatmap with correlation values
            heatmap = go.Figure(data=go.Heatmap(
                z=corr_matrix.values,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale="RdBu",
                text=corr_matrix.values,  # Add the correlation values as text
                texttemplate="%{text:.2f}",  # Format the text to 2 decimal places
                showscale=False  # Remove the color bar
            ))

            heatmap.update_layout(
                title="Correlation Matrix",
                xaxis_nticks=36
            )
            
            st.plotly_chart(heatmap)

        # Pair Plot
        pairplot_fig = px.scatter_matrix(
            df[["Churn", "TotalCharges", "tenure", "MonthlyCharges"]],
            dimensions=["TotalCharges", "tenure", "MonthlyCharges"],
            color="Churn",
            title="Pairplot"
        )
        st.plotly_chart(pairplot_fig)

        # Left, Middle, Right Columns for Countplots
        left, middle, right = st.columns(3)

        # Countplot for SeniorCitizen
        with left:
            countplot_fig = px.histogram(df, x="SeniorCitizen", color="Churn", barmode="group", title="Distribution of SeniorCitizen")
            st.plotly_chart(countplot_fig)

        # Countplot for InternetService
        with middle:
            countplot_fig = px.histogram(df, x="InternetService", color="Churn", barmode="group", title="Distribution of InternetService")
            st.plotly_chart(countplot_fig)

        # Countplot for Contract
        with right:
            countplot_fig = px.histogram(df, x="Contract", color="Churn", barmode="group", title="Distribution of Contract")
            st.plotly_chart(countplot_fig)


    if st.session_state["selected_dashboard"] == "Analytical Dashboard":
        # Title of dashboard
        left, middle, right = st.columns([1, 5, 1])
        with middle:
            st.markdown("<h1 style='color: lightblue;'> 💡 Churn Indicator Dashboard</h1>", unsafe_allow_html=True)

        # Sidebar widgets
        st.sidebar.header("Filter Options")

        # Tenure slider
        tenure = st.sidebar.slider("Tenure", 0, int(df["tenure"].max()), (0, int(df["tenure"].max())))

        # Total Charges range slider
        total_charges = st.sidebar.slider("Total Charges", float(df["TotalCharges"].min()), float(df["TotalCharges"].max()), (float(df["TotalCharges"].min()), float(df["TotalCharges"].max())))

        # Monthly Charges range slider
        monthly_charges = st.sidebar.slider("Monthly Charges", float(df["MonthlyCharges"].min()), float(df["MonthlyCharges"].max()), (float(df["MonthlyCharges"].min()), float(df["MonthlyCharges"].max())))

        # Filter the data based on sidebar input
        filtered_df = df[(df["tenure"] >= tenure[0]) & (df["tenure"] <= tenure[1]) &
                        (df["TotalCharges"] >= total_charges[0]) & (df["TotalCharges"] <= total_charges[1]) &
                        (df["MonthlyCharges"] >= monthly_charges[0]) & (df["MonthlyCharges"] <= monthly_charges[1])]


        # Calculate deltas for metrics
        total_monthly_charge = filtered_df["MonthlyCharges"].sum()
        total_charge = filtered_df["TotalCharges"].sum()
        total_customers_retained = len(filtered_df[filtered_df["Churn"] == "No"])
        churn_rate = (len(filtered_df[filtered_df["Churn"] == "Yes"]) / len(filtered_df)) * 100

        # Calculate unfiltered values
        unfiltered_monthly_charge = df["MonthlyCharges"].sum()
        unfiltered_total_charge = df["TotalCharges"].sum()
        unfiltered_customers_retained = len(df[df["Churn"] == "No"])

        # Calculate deltas
        monthly_charge_delta = (total_monthly_charge - unfiltered_monthly_charge) / unfiltered_monthly_charge * 100
        total_charge_delta = (total_charge - unfiltered_total_charge) / unfiltered_total_charge * 100
        customers_retained_delta = (total_customers_retained - unfiltered_customers_retained) / unfiltered_customers_retained * 100

    
        left_column, middle_column, right_column = st.columns(3)

        with left_column:
            st.metric("Total Monthly Charge", f"${total_monthly_charge/1e3:,.2f}K", delta=f"{monthly_charge_delta:.2f}%")

        with middle_column:
            st.metric("Total Charge", f"${total_charge/1e6:,.2f}M", delta=f"{total_charge_delta:.2f}%")

        with right_column:
            st.metric("Total Customers Retained", total_customers_retained, delta=f"{customers_retained_delta:.2f}%")


        # Row 1: Churn Rate by Tenure churn rate gauge
        col1, col2 = st.columns(2)
        with col1:
            churn_by_tenure = filtered_df.groupby("tenure")["Churn"].value_counts(normalize=True).unstack().fillna(0)
            fig_tenure = px.line(churn_by_tenure, y="Yes", title="Churn Rate by Tenure", width=450, height=300)
            st.plotly_chart(fig_tenure)

        with col2:
            gauge_fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = churn_rate,
                title = {"text": "Churn Rate (%)"},
                gauge = {
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "blue"},
                    "steps": [
                        {"range": [0, 30], "color": "lightgray"},
                        {"range": [30, 70], "color": "gray"},
                        {"range": [70, 100], "color": "red"}],
                    "threshold": {
                        "line": {"color": "black", "width": 4},
                        "thickness": 0.75,
                        "value": churn_rate}}))
            gauge_fig.update_layout(width=450, height=300)
            st.plotly_chart(gauge_fig)

        # Row 2: Churn Rate by Internet service and Churn Rate by Contract
        col1, col2 = st.columns(2)
        with col1:
            churn_by_internet_service = filtered_df[filtered_df["Churn"] == "Yes"].groupby("InternetService").size()
            fig_internet_service = px.pie(values=churn_by_internet_service, names=churn_by_internet_service.index, title="Churn Rate by InternetService", width=450, height=300)
            st.plotly_chart(fig_internet_service)

        with col2:
            churn_by_contract = filtered_df[filtered_df["Churn"] == "Yes"].groupby("Contract").size()
            fig_contract = px.bar(x=churn_by_contract.index, y=churn_by_contract.values, labels={"x":"Contract", "y":"Churn Rate (%)"}, title="Churn Rate by Contract", width=450, height=300)
            st.plotly_chart(fig_contract)

else:
    st.error("### The selected data source is empty!!!")






