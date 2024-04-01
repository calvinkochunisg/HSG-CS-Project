import requests
import streamlit as st

api_url = st.secrets["SPOONACULAR_URL_GENERATE_MEAL_PLAN"]
api_key = st.secrets["SPOONACULAR_KEY"]

def run():
    data = requests.get(api_url).json() #Need to fin out how to authenticate using api key: https://www.w3schools.com/python/ref_requests_get.asp, https://spoonacular.com/food-api/docs#Generate-Meal-Plan
    st.write(data)

