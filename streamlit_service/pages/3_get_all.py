import requests
import streamlit as st
from config import API_URL
from status_codes import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

endpoint = "/walruses/getall"

st.title("Get All Walruses")

if st.button("Get All Walruses"):
    response = requests.get(f"{API_URL}{endpoint}")
    if response.status_code == HTTP_200_OK:
        walruses_data = response.json()
        st.write("Walruses Data:")
        for walrus_data in walruses_data:
            st.write("Name:", walrus_data["name"])
            st.write("Friends:", walrus_data["friends"])
            st.write("Favorite Food:", walrus_data["favourite_food"])
            st.write("Birth Date:", walrus_data["birth_date"])
            st.write("---")
    elif response.status_code == HTTP_500_INTERNAL_SERVER_ERROR:
        st.error("Internal server error occurred. Please try again later.")
    else:
        st.error("Error occurred while fetching walruses data.")
