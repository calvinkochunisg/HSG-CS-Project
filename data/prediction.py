import subprocess
import requests
import pandas as pd
import json
import pickle
from io import BytesIO

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot

class Prediction:

    def parse(data):    
        parsed_data = data

    
        structured_nutrients = []

        # Iterate over each day in the data
        for day, content in parsed_data['week'].items():
            # Extract nutrients data and include the day of the week
            nutrients_data = {
                'Day': day.capitalize(),
                'calories': content['nutrients']['calories'],
                'Protein': content['nutrients']['protein'],
                'Fat': content['nutrients']['fat'],
                'Carbohydrates': content['nutrients']['carbohydrates']
            }
            # Append the nutrients data to the list
            structured_nutrients.append(nutrients_data)

        # Convert the list of nutrients data into a DataFrame
        user_cal = pd.DataFrame(structured_nutrients)
        user_cal = user_cal[["calories"]]
        return user_cal

    def convert(data, walk_days, run_days, weights_days, wine_days):
        user_cal = Prediction.parse(data)
        # get function for url
        week = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        walk = []
        run = []
        wine = []
        weights = []

        for day in week:
            if day in walk_days:
                walk.append(1)
            else:
                walk.append(0)

        for day in week:
            if day in run_days:
                run.append(1)
            else:
                run.append(0)

        for day in week:
            if day in wine_days:
                wine.append(1)
            else:
                wine.append(0)

        for day in week:
            if day in weights_days:
                weights.append(1)
            else:
                weights.append(0)

        user_rhy = pd.DataFrame({
                            'walk': walk,
                            'run': run,
                            'wine': wine,
                            'weight': weights})
        
        user_data = pd.concat([user_cal,user_rhy], axis=1)
        user_data.reset_index(drop=True, inplace=True)
        user_data.index = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        return user_data
    
    def pred(data_user, user_input1, user_input2, user_input3, user_input4, weight):
        url = "https://github.com/calvinkochunisg/HSG-CS-Project/raw/dev/Data/model.sav"
        user_data = Prediction.convert(data_user, user_input1, user_input2, user_input3, user_input4)
        weight_diff = 76.253 - weight
        
        response = requests.get(url)
        if response.status_code == 200:
            model_data = BytesIO(response.content)
            loaded_model = pickle.load(model_data)
            #adjusted weight
            prediction = loaded_model.predict(user_data) - weight_diff
            pred = pd.DataFrame(prediction, columns=['pred'])
            pred.reset_index(drop=True, inplace=True)
            pred.index = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            
            fig = plt.figure(figsize=(10, 5))
            host = host_subplot(111)
            par = host.twinx()

            host.set_xlabel("Your Weekday")
            host.set_ylabel("Your Body Weight")
            par.set_ylabel("Your Calory Intake")

            p1, = host.plot(user_data.index, pred, label="KG")
            p2, = par.plot(user_data.index, user_data["calories"], label="CAL")

            host.legend(labelcolor="linecolor")

            host.yaxis.get_label().set_color(p1.get_color())
            par.yaxis.get_label().set_color(p2.get_color())

            #plt.show()
            return fig

        else:
            print("Failed to download the file. Status code:", response.status_code)

        return None 

"""
Here the module can be testet, the following code will not be excecuted when importing the module somwhere else.

See Documentation of " if __name__ == "__main__": " here: https://realpython.com/if-name-main-python/
"""
if __name__ == "__main__":
    url_user = "https://api.spoonacular.com/mealplanner/generate?apiKey=4deaceca7a6448ba9d2006710177aad3&timeframe=week&diet=vegetarian"

    # Sample user inpput
    user_input1 = ["tue", "thu", "sun"] #walk
    user_input2 = ["mon", "thu", "sun"] #run
    user_input3  = ["tue", "wed", "sat"] #wine
    user_input4  = ["tue", "fri", "sun"] #weight
    user_weight = 65

    prediction = Prediction.pred(url_user, user_input1, user_input2, user_input3, user_input4,67)
