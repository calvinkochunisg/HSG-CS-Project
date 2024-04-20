#this will be the homepage, don't change the filename as it is needed by streamlit to acess. Other Classes etc. please add those to separate files and import them.

import streamlit as st
from api.spoonacular import SpoonacularAPI as sp
from api.ingredients import IngredientNames
from api.mealplan import MealPlan
from streamlit.logger import get_logger
from data.prediction import Prediction as pred

def Home():
    st.set_page_config(
        page_title="Foodplannerings",
        page_icon="🍲",
    )

    st.title('Prediction Inputs')
    WEEKDAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    VALID_DIETS = ["gluten_free", "ketogenic", "vegetarian", "lacto-vegetarian", "ovo-vegetarian", "vegan", "pescetarian", "paleo", "primal", "low_fodmap", "whole30"]
    VALID_INGREDIENTS = IngredientNames.get_ingredient_names()
    VALID_INTOLERANCES = ['dairy','egg','gluten','grain','peanut','seafood','sesame','shellfish','soy','sulfite','tree nut','wheat']
    EXCLUDE = VALID_INGREDIENTS + VALID_INTOLERANCES

    with st.expander('open options'):
        user_input1 = st.multiselect ('When do you go walking?', WEEKDAYS)
        user_input2 = st.multiselect ('When do you go running?', WEEKDAYS)
        user_input3 = st.multiselect ('When do you drink wine?', WEEKDAYS)
        user_input4 = st.multiselect ('When do you go lift weights?', WEEKDAYS)
        user_weight = st.number_input("Bodyweight", value=60, min_value = 0, max_value = 500, placeholder="Insert your current bodyweight in kg ...")
        
    st.title('Mealplan Inputs')
    with st.expander('open options'):
        targetCalories = st.number_input("Target Calories", value=None, min_value = 0, max_value = 10000, placeholder="Insert your target Calories in kcal ...")
        diet = st.multiselect ('Do you follow any special diets?', VALID_DIETS)
        exclude = st.multiselect ('Is there something you cannot eat?', EXCLUDE)

    if st.button('Generate Meal Plan'):
        
        sp_meal = sp()
        url_user = sp_meal.generate_meal_plan(targetCalories, diet, exclude)

        prediction = pred.pred(url_user, user_input1, user_input2, user_input3, user_input4, user_weight)
        st.write(prediction)

        mealplan = MealPlan(url_user)

        day = st.selectbox('Select a day', ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
        meals = mealplan.get_day_mealplan(day)

        st.write(f"Meals for {day}:")
        for i, meal in enumerate(meals):
            st.write(f"Meal {i+1}: {meal['title']}")

        nutrients = mealplan.get_nutrient_info(day)
        st.write(f"Nutrient info for {day}: {nutrients}")
Home()