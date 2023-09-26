import requests
import streamlit as st
from config import API_URL
from status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND

endpoint = "/walruses/delete"

st.title("Delete Walrus by Name")
name = st.text_input("Enter the name of the walrus")

if st.button("Delete Walrus"):
    if name:
        response = requests.delete(f"{API_URL}{endpoint}/{name}")
        if response.status_code == HTTP_200_OK:
            st.success(f"Walrus '{name}' deleted successfully!")
        elif response.status_code == HTTP_404_NOT_FOUND:
            st.error(f"Walrus '{name}' not found.")
        else:
            st.error(
                "Error occurred while deleting the walrus:" f"{response.text}"
            )
    else:
        st.warning("Please enter the name of the walrus.")
