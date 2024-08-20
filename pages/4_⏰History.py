import streamlit as st
import pandas as pd


# Set up Home page
st.set_page_config(page_title = "Customer Churn Prediction App", page_icon = "🔭", layout = "wide")

st.markdown("<h1 style='color: lightblue;'> ⏰ Customer Churn Prediction History</h1>", unsafe_allow_html=True)

@st.cache_data(persist = True)
def load_data():
    data = pd.read_csv("./data/history.csv")
    return data
        
data = load_data()
        
# Display data preview
st.dataframe(data)



# history_df = pd.DataFrame(data)
# history_df['PredictionDate'] = pd.to_datetime(history_df['PredictionDate'])

# # Streamlit App Title
# st.title("Churn Prediction History")

# # Sidebar for interactive filters
# st.sidebar.header("Filters")

# # Date range filter
# date_range = st.sidebar.date_input("Select Date Range", [history_df['PredictionDate'].min(), history_df['PredictionDate'].max()])
# filtered_df = history_df[(history_df['PredictionDate'] >= pd.to_datetime(date_range[0])) &
#                          (history_df['PredictionDate'] <= pd.to_datetime(date_range[1]))]

# # Search by Customer ID or Name
# search_query = st.sidebar.text_input("Search by Customer ID or Name")
# if search_query:
#     filtered_df = filtered_df[
#         filtered_df['CustomerID'].str.contains(search_query, case=False) |
#         filtered_df['CustomerName'].str.contains(search_query, case=False)
#     ]

# # Filter by Churn Prediction
# churn_filter = st.sidebar.multiselect("Filter by Prediction Outcome", options=['Churn', 'No Churn'], default=['Churn', 'No Churn'])
# filtered_df = filtered_df[filtered_df['ChurnPrediction'].isin(churn_filter)]

# # Display the filtered DataFrame
# st.subheader("Filtered Prediction History")
# st.write(filtered_df)

# # Additional option: download filtered data
# if not filtered_df.empty:
#     csv = filtered_df.to_csv(index=False)
#     st.download_button(
#         label="Download Filtered Data as CSV",
#         data=csv,
#         file_name='filtered_prediction_history.csv',
#         mime='text/csv',
#     )
