import subprocess
import requests
import pandas as pd
import json
import pickle
from io import BytesIO

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot

class Prediction:
    # Static method to parse nutrient data from the API response.
    def parse(data):    
        """
        Parses the nutrient data for a week and structures it in a list.

        :param data: The raw data from the Spoonacular API.
        :return: A DataFrame containing only the calories information.
        """
        parsed_data = data  # The raw data received from the API.
        structured_nutrients = []  # Initialize a list to hold structured nutrient data.

        # Loop through each day provided in the data.
        for day, content in parsed_data['week'].items():
            # Create a dictionary of the nutrient data for the current day.
            nutrients_data = {
                'Day': day.capitalize(),  # Capitalize the day name for presentation.
                'calories': content['nutrients']['calories'],
                'Protein': content['nutrients']['protein'],
                'Fat': content['nutrients']['fat'],
                'Carbohydrates': content['nutrients']['carbohydrates']
            }
            # Append the structured nutrient data to the list.
            structured_nutrients.append(nutrients_data)

        # Convert the structured nutrient data list to a DataFrame.
        user_cal = pd.DataFrame(structured_nutrients)
        user_cal = user_cal[["calories"]]  # Filter only the calories column.
        return user_cal

    # Static method to combine user routine data with calorie data.
    def convert(data, walk_days, run_days, weights_days, wine_days):
        """
        Combines user routine data with the calorie data to form a complete dataset.

        :param data: Calorie data as a DataFrame.
        :param walk_days: List of days the user goes walking.
        :param run_days: List of days the user goes running.
        :param weights_days: List of days the user lifts weights.
        :param wine_days: List of days the user drinks wine.
        :return: A DataFrame with the combined user routine and calorie data.
        """
        user_cal = Prediction.parse(data)  # Parse the calorie data.
        # Lists to hold user routine data, initialized to zeros.
        walk = [1 if day in walk_days else 0 for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]]
        run = [1 if day in run_days else 0 for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]]
        wine = [1 if day in wine_days else 0 for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]]
        weights = [1 if day in weights_days else 0 for day in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]]

        # Create a DataFrame with the user routine data.
        user_rhy = pd.DataFrame({
                            'walk': walk,
                            'run': run,
                            'wine': wine,
                            'weight': weights})
        
        # Combine the calorie data and routine data into a single DataFrame.
        user_data = pd.concat([user_cal, user_rhy], axis=1)
        user_data.reset_index(drop=True, inplace=True)
        user_data.index = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        return user_data
    
    # Static method to predict user weight change based on routine and calorie intake.
    def pred(data_user, user_input1, user_input2, user_input3, user_input4, weight):
        """
        Predicts the user's weight based on their routine, calorie intake, and initial weight.

        :param data_user: User data for the routine and calories.
        :param user_input1: List of walk days.
        :param user_input2: List of run days.
        :param user_input3: List of wine days.
        :param user_input4: List of weight lifting days.
        :param weight: The user's initial weight.
        :return: A matplotlib figure object containing the plotted predictions.
        """
        # URL pointing to the stored machine learning model.
        url = "https://github.com/calvinkochunisg/HSG-CS-Project/raw/dev/Data/model.sav"
        # Prepare user data for prediction.
        user_data = Prediction.convert(data_user, user_input1, user_input2, user_input3, user_input4)
        # Calculate the difference from a reference weight for adjustment.
        weight_diff = 76.253 - weight
        
        # Fetch the model from the provided URL.
        response = requests.get(url)
        if response.status_code == 200:
            # Read the model binary data.
            model_data = BytesIO(response.content)
            # Load the model from the binary data.
            loaded_model = pickle.load(model_data)
            # Adjust weight and make predictions using the loaded model.
            prediction = loaded_model.predict(user_data) - weight_diff
            # Convert the prediction to a DataFrame for plotting.
            pred = pd.DataFrame(prediction, columns=['pred'])
            pred.reset_index(drop=True, inplace=True)
            pred.index = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            
            # Create a plot with dual axes to show weight and calorie intake.
            fig = plt.figure(figsize=(10, 5))
            host = host_subplot(111)
            par = host.twinx()

            host.set_xlabel("Your Weekday")
            host.set_ylabel("Your Body Weight")
            par.set_ylabel("Your Calory Intake")

            # Plot the predictions and calorie intake on the respective axes.
            p1, = host.plot(user_data.index, pred, label="KG")
            p2, = par.plot(user_data.index, user_data["calories"], label="CAL")

            host.legend(loc='best', labelcolor="linecolor")

            host.yaxis.get_label().set_color(p1.get_color())
            par.yaxis.get_label().set_color(p2.get_color())

            #plt.show()
            return fig

        else:
            print("Failed to download the file. Status code:", response.status_code)

        return None 
