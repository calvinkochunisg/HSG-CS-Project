class MealPlan:
    def __init__(self, data):
        self.data = data

    def get_day_mealplan(self, day):
        # Access the day's data from self.data
        return self.data['week'][day]['meals']

    def get_nutrient_info(self, day):
        # Return nutrient info for the specified day
        return self.data['week'][day]['nutrients']