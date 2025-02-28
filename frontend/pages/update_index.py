import streamlit as st
import requests
from config import API_BASE_URL

st.set_page_config(page_title="Update Index", page_icon="🔄")

st.title("🔄 Update Index")
st.write("Click the button below to refresh the index after updating job profiles.")

if st.button("🔄 Update Index"):
    response = requests.post("{API_BASE_URL}/update_index/")
    
    if response.status_code == 200:
        st.success(response.json()["message"])
    else:
        st.error("Failed to update index. Please check the server.")
