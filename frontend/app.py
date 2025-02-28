import streamlit as st
import requests
import os

from config import API_BASE_URL


st.set_page_config(page_title="JobMentorAI", page_icon="🎓")

st.title("🎓 JobMentorAI")

st.sidebar.title("🔝 Career Advisory AI")
st.sidebar.markdown("**AI-powered job mentoring**\n\nHelping you find the best career paths! 🚀")

st.sidebar.markdown("---")
# Sidebar link to update index
st.sidebar.page_link("pages/update_index.py", label="🔄 Update Index")  

# text input for user query
query = st.text_input("Find the best job! (Enter skills, degree, or career goal):")

# a button to trigger the job search
if st.button("🔍 Click Me!"):
    if query.strip():  # ensure the input is not empty
        response = requests.get(f"{API_BASE_URL}/query/?query={query}").json()
        
        st.write("### 🤖 AI Resppnse")
        st.write(response["response"])

        with st.expander("Please click here for context"):
            st.write(response["retrieved_context"])
    else:
        st.warning("Please enter your skills, degree, or job interest before searching.")
