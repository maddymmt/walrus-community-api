import requests
import streamlit as st
from config import API_URL
from status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND

endpoint = "/walruses/get"

st.title("Get Walrus by Name")
name = st.text_input("Enter the name of the walrus")

if st.button("Get Walrus"):
    if name:
        url = f"{API_URL}{endpoint}?name={name}"
        response = requests.get(url)
        if response.status_code == HTTP_200_OK:
            walrus_data = response.json()
            st.write("Walrus Data:")
            st.write("Name:", walrus_data["name"])
            st.write("Friends:", walrus_data["friends"])
            st.write("Favorite Food:", walrus_data["favourite_food"])
            st.write("Birth Date:", walrus_data["birth_date"])
        elif response.status_code == HTTP_404_NOT_FOUND:
            st.warning("Walrus not found.")
        else:
            st.error("Error occurred while fetching walrus data.")
    else:
        st.warning("Please enter the name of the walrus.")
