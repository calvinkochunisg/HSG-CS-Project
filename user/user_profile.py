class UserProfile:
    def __init__(self, height, weight, age, gender, activity_type, diet, exclude):
        self.height = height
        self.weight = weight
        self.age = age
        self.gender = gender
        self.activity_type = activity_type
        self.diet = diet
        self.exclude = exclude

        self.basal_metabolic_rate = self.calculate_bmr()
        self.activity_factor = self.get_activity_factor()
        self.calories_needed = self.basal_metabolic_rate * self.activity_factor

        # Setting default walking, running, wine, and weights days based on activity type
        self.set_activity_days()

    def calculate_bmr(self):
        # Calculate Basal Metabolic Rate (BMR) using the Harris-Benedict equation
        # Source: https://www.calculator.net/calorie-calculator.html
        if self.gender == 'Male':
            bmr = 13.397 * self.weight + 4.799 * self.height - 5.677 * self.age + 88.362
        else:
            bmr = 9.247 * self.weight + 3.098 * self.height - 4.330 * self.age + 447.593
        return bmr

    def get_activity_factor(self):
        # Maps the activity type to an activity factor
        activity_factors = {
            "Sedentary": 1.2,
            "Light": 1.375,
            "Moderate": 1.55,
            "Active": 1.725,
            "Very Active": 1.9,
            "Extra Active": 2.0

        }
        return activity_factors.get(self.activity_type, 1.2)  # Default to sedentary if not found

    def set_activity_days(self):
        # Set the default weekdays based on activity type
        if self.activity_type == 'Moderate':
            self.walking_days = ['mon', 'wed', 'fri']
            self.running_days = ['tue', 'sat']
            self.wine_days = ['wed', 'fri', 'sat', 'sun']
            self.weights_days = ['wed']
        elif self.activity_type == 'Active':
            self.walking_days = ['mon', 'tue', 'wed', 'thu', 'fri']
            self.running_days = ['mon', 'tue', 'thu', 'sat']
            self.wine_days = ['sat', 'sun']
            self.weights_days = ['mon', 'wed', 'sat']
        elif self.activity_type == 'Very Active':
            self.walking_days = ['mon', 'tue', 'wed', 'thu', 'fri']
            self.running_days = ['sat', 'sun']
            self.wine_days = []
            self.weights_days = ['sun']
        elif self.activity_type == 'Extra Active':
            self.walking_days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
            self.running_days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
            self.wine_days = []
            self.weights_days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        else:
            # Default to light activity
            self.walking_days = ['mon', 'wed', 'fri']
            self.running_days = ['tue', 'thu']
            self.wine_days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
            self.weights_days = ['sun'] 

