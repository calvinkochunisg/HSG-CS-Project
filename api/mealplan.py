from api.spoonacular import SpoonacularAPI as sp
from collections import defaultdict

class MealPlan:
    """
    A class representing a meal plan, which contains information about meals and nutrients
    for each day of the week.
    """
    
    def __init__(self, data):
        """
        Initializes a new instance of MealPlan with the provided data.
        
        :param data: A dictionary containing meal plan data for the week.
        """
        self.data = data
        self.recipe_cache = {}  # A cache to store recipe details to avoid redundant API calls.

    def get_day_meal_ids(self, day):
        """
        Retrieves all meal IDs for the specified day.
        
        :param day: A string representing the day of the week.
        :return: A list of meal IDs.
        """
        return [meal['id'] for meal in self.data['week'][day]['meals']]

    def get_day_meals(self, day):
        """
        Retrieves all meal information for the specified day.
        
        :param day: A string representing the day of the week.
        :return: A list of meal details for the day.
        """
        return self.data['week'][day]['meals']

    def get_nutrient_info(self, day):
        """
        Retrieves the nutrient information for the specified day.
        
        :param day: A string representing the day of the week.
        :return: A dictionary containing nutrient information.
        """
        return self.data['week'][day]['nutrients']
    
    def get_recipe_information(self, api, recipe_id):
        """
        Retrieves recipe information, either from the cache or by making an API call.
        
        :param api: An instance of SpoonacularAPI.
        :param recipe_id: An integer ID of the recipe.
        :return: A dictionary containing recipe information.
        """
        # If recipe information is not in the cache, retrieve it from the API.
        if recipe_id not in self.recipe_cache:
            recipe_info = api.get_recipe_information(recipe_id)
            if recipe_info:
                # Cache the information for future use.
                self.recipe_cache[recipe_id] = recipe_info
        return self.recipe_cache.get(recipe_id, None)

    def get_ingredients_for_day(self, day, api):
        """
        Aggregates all ingredients needed for the meals of a specified day.
        
        :param day: A string representing the day of the week.
        :param api: An instance of SpoonacularAPI.
        :return: A list of aggregated ingredients with their amounts and units.
        """
        ingredient_aggregator = defaultdict(float)
        meal_ids = self.get_day_meal_ids(day)
        for meal_id in meal_ids:
            recipe_info = self.get_recipe_information(api, meal_id)
            if recipe_info and 'extendedIngredients' in recipe_info:
                for item in recipe_info['extendedIngredients']:
                    # Create a unique key for each ingredient including its unit.
                    key = (item['name'], item.get('unit', ''))
                    # Aggregate the amount needed for this ingredient.
                    ingredient_aggregator[key] += item.get('amount', 0)
        # Convert the aggregated ingredients into a list of dictionaries.
        aggregated_ingredients = [{'amount': amt, 'unit': unit, 'ingredient': name} 
                                  for (name, unit), amt in ingredient_aggregator.items()]
        return aggregated_ingredients
    
    def get_ingredients_for_week(self, api):
        """
        Aggregates all ingredients needed for the entire week.
        
        :param api: An instance of SpoonacularAPI.
        :return: A list of aggregated ingredients with their amounts and units for the week.
        """
        weekly_ingredient_aggregator = defaultdict(float)
        for day in self.data['week']:
            day_ingredients = self.get_ingredients_for_day(day, api)
            for ingredient in day_ingredients:
                key = (ingredient['ingredient'], ingredient['unit'])
                weekly_ingredient_aggregator[key] += ingredient['amount']
        aggregated_ingredients = [{'amount': amt, 'unit': unit, 'ingredient': name} 
                                  for (name, unit), amt in weekly_ingredient_aggregator.items()]
        return aggregated_ingredients
    
    def get_nutrients_for_week(self):
        """
        Aggregates nutrient information for the entire week.
        
        :return: A dictionary with total amount of each nutrient for the week.
        """
        week_nutrients = {'calories': 0, 'protein': 0, 'fat': 0, 'carbohydrates': 0}
        for day in self.data['week']:
            day_nutrients = self.get_nutrient_info(day)
            for nutrient, amount in day_nutrients.items():
                week_nutrients[nutrient] += amount
        return week_nutrients

class Meal:
    """
    A class representing a single meal, which includes a title and a list of ingredients.
    """
    
    def __init__(self, id, title, ingredients):
        """
        Initializes a new instance of Meal with the given ID, title, and ingredients.
        
        :param id: An integer ID of the meal.
        :param title: A string title of the meal.
        :param ingredients: A list of strings, each representing an ingredient.
        """
        self.id = id
        self.title = title
        self.ingredients = ingredients

    def __str__(self):
        """
        Returns a string representation of the meal, including its title and ingredients.
        
        :return: A string.
        """
        return f"{self.title} (ID: {self.id}): Ingredients - {', '.join(self.ingredients)}"
