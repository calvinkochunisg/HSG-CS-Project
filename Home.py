import streamlit as st
from api.spoonacular import SpoonacularAPI as sp
from api.ingredients import IngredientNames
from api.mealplan import MealPlan
from streamlit.logger import get_logger
from data.prediction import Prediction as pred
import pandas as pd

def Home():
    st.set_page_config(
        page_title="Foodplannerings",
        page_icon="🍲",
    )

    st.title('Prediction Inputs')
    WEEKDAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    VALID_DIETS = ["gluten_free", "ketogenic", "vegetarian", "lacto-vegetarian", "ovo-vegetarian", "vegan", "pescetarian", "paleo", "primal", "low_fodmap", "whole30"]
    VALID_INGREDIENTS = IngredientNames.get_ingredient_names()
    VALID_INTOLERANCES = ['dairy', 'egg', 'gluten', 'grain', 'peanut', 'seafood', 'sesame', 'shellfish', 'soy', 'sulfite', 'tree nut', 'wheat']
    EXCLUDE = VALID_INGREDIENTS + VALID_INTOLERANCES

    with st.expander('open options'):
        user_input1 = st.multiselect('When do you go walking?', WEEKDAYS)
        user_input2 = st.multiselect('When do you go running?', WEEKDAYS)
        user_input3 = st.multiselect('When do you drink wine?', WEEKDAYS)
        user_input4 = st.multiselect('When do you lift weights?', WEEKDAYS)
        user_weight = st.number_input("Bodyweight", value=60, min_value=0, max_value=500, placeholder="Insert your current bodyweight in kg ...")
        
    st.title('Mealplan Inputs')
    with st.expander('open options'):
        targetCalories = st.number_input("Target Calories", value=2000, min_value=0, max_value=10000, placeholder="Insert your target Calories in kcal ...")
        diet = st.multiselect('Do you follow any special diets?', VALID_DIETS)
        exclude = st.multiselect('Is there something you cannot eat?', EXCLUDE)

    if st.button('Generate Meal Plan'):
        sp_meal = sp()
        meal_data = sp_meal.generate_meal_plan(targetCalories, diet, exclude)

        if meal_data:
            prediction = pred.pred(meal_data, user_input1, user_input2, user_input3, user_input4, user_weight)
            mealplan = MealPlan(meal_data)

            # Use the prediction and mealplan objects as needed
            # (Your existing code to display predictions and meal plans...)

            st.session_state['meal_plan_data'] = {
                'prediction': prediction,
                'mealplan': mealplan,
            }

    if 'meal_plan_data' in st.session_state:
        prediction = st.session_state['meal_plan_data']['prediction']
        mealplan = st.session_state['meal_plan_data']['mealplan']

        # Select a day to display meals and nutrients
        day = st.selectbox('Select a day', ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
        meals = mealplan.get_day_meals(day)
        nutrients = mealplan.get_nutrient_info(day)
        sp_api = sp()  # Initialize the API object

        # Display meal information
        st.write(f"Meals for {day}:")
        for i, meal in enumerate(meals):
            st.write(f"Meal {i+1}: {meal['title']}")
        
        st.write(f"Nutrient info for {day}:")
        nutrients = mealplan.get_nutrient_info(day)
        if nutrients:
            # Convert nutrient dict to pandas DataFrame for plotting
            nutrients_df = pd.DataFrame(list(nutrients.items()), columns=['Nutrient', 'Amount'])
            st.bar_chart(nutrients_df.set_index('Nutrient'))

        # Display predictions if available
        if prediction:
            st.pyplot(prediction)

        if st.button('Generate Ingredient Lists'):
            sp_api = sp()
            # Fetch and store ingredients for the selected day and whole week
            st.session_state['day_ingredients'] = mealplan.get_ingredients_for_day(day, sp_api)
            st.session_state['week_ingredients'] = mealplan.get_ingredients_for_week(sp_api)

        # Display daily ingredients if available
        if 'day_ingredients' in st.session_state and st.session_state['day_ingredients']:
            with st.expander(f"Show Ingredients for {day}"):
                daily_df = pd.DataFrame(st.session_state['day_ingredients'])
                st.table(daily_df[['amount', 'unit', 'ingredient']].sort_values('ingredient'))

        # Display weekly ingredients if available
        if 'week_ingredients' in st.session_state and st.session_state['week_ingredients']:
            with st.expander("Show Ingredients for the Whole Week"):
                weekly_df = pd.DataFrame(st.session_state['week_ingredients'])
                st.table(weekly_df[['amount', 'unit', 'ingredient']].sort_values('ingredient'))

        # ... (logic to display the nutrient info bar chart)





Home()