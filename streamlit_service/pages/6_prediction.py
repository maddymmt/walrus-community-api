import requests
import streamlit as st
from config import API_URL
from status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND

endpoint = "/walruses/getprediction"

st.title("Walrus Prediction")

name = st.text_input("Enter the name of the walrus")

if st.button("Get Prediction"):
    if name:
        url = f"{API_URL}{endpoint}?name={name}"
        response = requests.get(url)
        if response.status_code == HTTP_200_OK:
            prediction_data = response.json()
            prediction = prediction_data["prediction"]
            st.success(prediction)
        elif response.status_code == HTTP_404_NOT_FOUND:
            st.error("Walrus not found.")
        else:
            st.error("Error occurred while fetching the prediction.")
    else:
        st.warning("Please enter the name of the walrus.")
