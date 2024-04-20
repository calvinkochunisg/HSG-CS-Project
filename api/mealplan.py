import requests

class MealPlan:
    def __init__(self, url):
        response = requests.get(url)
        response.raise_for_status()  # Raises a HTTPError if the response was an error
        self._mealplan = response.json()

    def get_day_mealplan(self, day):
        return self._mealplan['week'][day]['meals']

    def get_meal_info(self, day, meal_index):
        return self._mealplan['week'][day]['meals'][meal_index]

    def get_nutrient_info(self, day):
        return self._mealplan['week'][day]['nutrients']