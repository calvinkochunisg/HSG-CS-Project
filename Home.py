import streamlit as st
# Import necessary modules and classes from the application's packages
from api.spoonacular import SpoonacularAPI as sp
from api.ingredients import IngredientNames
from api.mealplan import MealPlan
from user.user_profile import UserProfile
from streamlit.logger import get_logger
from data.prediction import Prediction as pred
import pandas as pd

# Define the main function for the Streamlit application
def Home():
    # Configure the page with a title and an icon
    st.set_page_config(
        page_title="Foodplannerings",
        page_icon="🍲",
    )

    # Display the main title on the page
    st.title('Prediction Inputs')
    # Predefined lists of valid options for diet and intolerances
    VALID_DIETS = ["gluten_free", "ketogenic", "vegetarian", "lacto-vegetarian", "ovo-vegetarian", "vegan", "pescetarian", "paleo", "primal", "low_fodmap", "whole30"]
    VALID_INGREDIENTS = IngredientNames.get_ingredient_names()
    VALID_INTOLERANCES = ['dairy', 'egg', 'gluten', 'grain', 'peanut', 'seafood', 'sesame', 'shellfish', 'soy', 'sulfite', 'tree nut', 'wheat']
    EXCLUDE = VALID_INGREDIENTS + VALID_INTOLERANCES

    # Create a collapsible section for user inputs
    with st.expander('User Inputs'):
        # Collect user inputs for various personal details
        height = st.number_input('Height (cm)', value=180, min_value=0, max_value=250, placeholder="Insert your current height in cm ...")
        weight = st.number_input('Weight (kg)', value=60, min_value=0, max_value=500, placeholder="Insert your current bodyweight in kg ...")
        age = st.number_input('Age', value=30, min_value=0, max_value=150, placeholder="Insert your current age in years ...")
        gender = st.radio('Biological Gender', ['Male', 'Female'])
        activity_type = st.radio('Activity Level', ['Light', 'Moderate', 'Active', 'Very Active', 'Extra Active'])
        diet = st.multiselect('Do you follow any special diets?', VALID_DIETS)
        exclude = st.multiselect('Is there something you cannot eat?', EXCLUDE)
        # Initialize a UserProfile object with the collected inputs
        user_profile = UserProfile(height, weight, age, gender, activity_type, diet, exclude)
        # Display the calculated calories needed per day
        st.text(f'Calories needed per day: {user_profile.calories_needed:.2f} kcal')
        
    # Button to generate a meal plan based on the user inputs
    if st.button('Generate Meal Plan'):
        # Initialize the Spoonacular API client
        sp_meal = sp()
        # Request the meal data from the Spoonacular API
        meal_data = sp_meal.generate_meal_plan(user_profile.calories_needed, user_profile.diet, user_profile.exclude)

        # If meal data was successfully received
        if meal_data:
            # Generate predictions for weight change and meal plan details
            prediction = pred.pred(meal_data, user_profile.walking_days, user_profile.running_days, user_profile.wine_days, user_profile.weights_days, user_profile.weight)
            mealplan = MealPlan(meal_data)
            # Store prediction and meal plan information in the session state
            st.session_state['meal_plan_data'] = {
                'prediction': prediction,
                'mealplan': mealplan,
            }

    # If meal plan data is available in the session state
    if 'meal_plan_data' in st.session_state:
        st.divider() # Add a visual divider in the app
        # Retrieve prediction and meal plan data from the session state
        prediction = st.session_state['meal_plan_data']['prediction']
        mealplan = st.session_state['meal_plan_data']['mealplan']
        # Initialize the Spoonacular API client
        sp_api = sp()

        # Create a dropdown for the user to select a specific day or the whole week
        options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'Whole Week']
        day = st.selectbox('Select a day', options)

        # If the user selects 'Whole Week'
        if day == 'Whole Week':
            # Call function to display meals for the entire week
            display_weekly_meals(mealplan, sp_api)
            # Try to display the nutrient information for the whole week
            try:
                week_nutrients = mealplan.get_nutrients_for_week()
                st.subheader('Nutrient Information - Whole Week')
                # Convert nutrients data into a DataFrame and display it as a bar chart
                week_nutrients_df = pd.DataFrame(list(week_nutrients.items()), columns=['Nutrient', 'Amount'])
                st.bar_chart(week_nutrients_df.set_index('Nutrient'))
            except Exception as e:
                # Display an error message if something goes wrong
                st.error(f"Could not retrieve nutrient information for the whole week. Error: {e}")
        else:
            # Display meals for the selected day
            st.subheader(f'Mealplan Information for {day}')
            display_day_meals(day.lower(), mealplan, sp_api)
            # Try to handle nutrient information for the selected day
            try:
                nutrients = mealplan.get_nutrient_info(day.lower())
                if nutrients:
                    st.subheader(f'Nutrient Information for {day}')
                    # Convert nutrients data into a DataFrame and display it as a bar chart
                    nutrients_df = pd.DataFrame(list(nutrients.items()), columns=['Nutrient', 'Amount'])
                    st.bar_chart(nutrients_df.set_index('Nutrient'))
            except KeyError:
                # Display an error message if nutrient information is not available
                st.error(f"Nutrient information for {day} is not available.")

        # Display predictions if they are available
        if prediction:
            st.divider() # Add a visual divider in the app
            st.subheader('Weight Prediction')
            st.pyplot(prediction)

        # Section for generating and displaying the shopping list
        st.divider() # Add a visual divider in the app
        st.subheader('Shopping List')
        if st.button('Generate Shopping Lists'):
            sp_api = sp()
            # Fetch and store ingredients for the selected day and the entire week
            if day != 'Whole Week':
                st.session_state['day_ingredients'] = mealplan.get_ingredients_for_day(day.lower(), sp_api)
            st.session_state['week_ingredients'] = mealplan.get_ingredients_for_week(sp_api)

        # Check if daily ingredients are available and display them
        if 'day_ingredients' in st.session_state and st.session_state['day_ingredients']:
            with st.expander(f"Show Shopping List for {day}"):
                # Convert the ingredients list to a DataFrame and display it
                daily_df = pd.DataFrame(st.session_state['day_ingredients'])
                daily_df = daily_df[['amount', 'unit', 'ingredient']].sort_values('ingredient')
                st.dataframe(daily_df, hide_index=True, use_container_width=True)

        # Check if weekly ingredients are available and display them
        if 'week_ingredients' in st.session_state and st.session_state['week_ingredients']:
            with st.expander("Show Shopping List for the Whole Week"):
                # Convert the ingredients list to a DataFrame and display it
                weekly_df = pd.DataFrame(st.session_state['week_ingredients'])
                weekly_df = weekly_df[['amount', 'unit', 'ingredient']].sort_values('ingredient')
                st.dataframe(weekly_df, hide_index=True, use_container_width=True)

# Function to display the meals for the whole week
def display_weekly_meals(mealplan, sp_api):
    WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    meal_labels = ["Breakfast", "Lunch", "Dinner"]  # Labels for the meals

    for day in WEEKDAYS:
        st.markdown(f"#### {day}")
        display_day_meals(day.lower(), mealplan, sp_api)

# Function to display the meals for a specific day
def display_day_meals(day, mealplan, sp_api):
    meals = mealplan.get_day_meals(day)
    meal_labels = ["Breakfast", "Lunch", "Dinner"]  # Move this inside the function
    cols = st.columns(3)
    for i, meal in enumerate(meals):
        meal_info = mealplan.get_recipe_information(sp_api, meal['id'])
        if meal_info:
            with cols[i % 3]:
                st.caption(meal_labels[i % len(meal_labels)])
                st.image(meal_info['image'], width=200)
                st.markdown(f"**{meal['title']}**")

# Call the main function to run the app
Home()
