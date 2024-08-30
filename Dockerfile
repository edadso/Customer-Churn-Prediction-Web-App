# Use the official Python 3.12 slim image as the base image
FROM python:3.12.5-slim

# Set the maintainer, and author
LABEL maintainer="emmanueldadson36@gmail.com"
LABEL author="Emmanuel Dadson"

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt /app/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app's code into the container
COPY . /app/

# Expose the port Streamlit runs on (default is 8501)
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "🏠Home.py", "--server.port=8501", "--server.address=0.0.0.0"]
