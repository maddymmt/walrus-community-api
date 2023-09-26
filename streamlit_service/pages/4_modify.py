import requests
import streamlit as st
from config import API_URL
from status_codes import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

endpoint = "/walruses/modify"

st.title("Modify Walrus Favorite Food")
name = st.text_input("Enter the name of the walrus")
favourite_food = st.text_input("Enter the new favorite food")

if st.button("Modify"):
    if name and favourite_food:
        url = f"{API_URL}{endpoint}/{name}?favourite_food={favourite_food}"
        response = requests.put(url)
        if response.status_code == HTTP_200_OK:
            st.success(f"Walrus '{name}' modified successfully!")
        elif response.status_code == HTTP_404_NOT_FOUND:
            st.error(f"Walrus '{name}' not found.")
        elif response.status_code == HTTP_400_BAD_REQUEST:
            st.error("Invalid request. Please provide valid data.")
        else:
            st.error(
                f"Error occurred while modifying the walrus: {response.text}"
            )
    else:
        st.warning("Please enter both name and favorite food.")
