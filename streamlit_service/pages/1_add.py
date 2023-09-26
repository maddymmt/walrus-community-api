import requests
import streamlit as st
from config import API_URL
from status_codes import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

endpoint = "/walruses/add"
st.title("Add Walrus")
name = st.text_input("Enter the name of the walrus")
friends = st.text_input("Enter the friends of the walrus (comma-separated)")
favourite_food = st.text_input("Enter the favourite food of the walrus")
birth_date = st.date_input("Enter the birth date of the walrus")

if st.button("Add Walrus"):
    if name and favourite_food and birth_date:
        friends_list = friends.split(",") if friends else []
        payload = {
            "name": name,
            "friends": friends_list,
            "favourite_food": favourite_food,
            "birth_date": str(birth_date),
        }
        response = requests.post(f"{API_URL}{endpoint}", json=payload)
        if response.status_code == HTTP_201_CREATED:
            st.success(f"Walrus '{name}' added successfully!")
        elif response.status_code == HTTP_400_BAD_REQUEST:
            st.error("Invalid request. Please provide unique walrus name.")
        else:
            st.error(
                f"Error occurred while adding the walrus: {response.text}"
            )
    else:
        st.warning("Please enter the required information.")
