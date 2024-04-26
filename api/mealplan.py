from api.spoonacular import SpoonacularAPI as sp
from collections import defaultdict

class MealPlan:
    def __init__(self, data):
        self.data = data
        self.recipe_cache = {}  # Cache to store recipe details

    def get_day_meal_ids(self, day):
        return [meal['id'] for meal in self.data['week'][day]['meals']]

    def get_day_meals(self, day):
        return self.data['week'][day]['meals']

    def get_nutrient_info(self, day):
        return self.data['week'][day]['nutrients']
    
    def get_recipe_information(self, api, recipe_id):
        # Check if recipe information is already in cache
        if recipe_id not in self.recipe_cache:
            recipe_info = api.get_recipe_information(recipe_id)
            if recipe_info:
                self.recipe_cache[recipe_id] = recipe_info
        return self.recipe_cache.get(recipe_id, None)

    def get_ingredients_for_day(self, day, api):
        ingredient_aggregator = defaultdict(float)
        meal_ids = self.get_day_meal_ids(day)
        for meal_id in meal_ids:
            recipe_info = self.get_recipe_information(api, meal_id)
            if recipe_info and 'extendedIngredients' in recipe_info:
                for item in recipe_info['extendedIngredients']:
                    key = (item['name'], item.get('unit', ''))
                    ingredient_aggregator[key] += item.get('amount', 0)
        aggregated_ingredients = [{'amount': amt, 'unit': unit, 'ingredient': name} for (name, unit), amt in ingredient_aggregator.items()]
        return aggregated_ingredients
    
    def get_ingredients_for_week(self, api):
        weekly_ingredient_aggregator = defaultdict(float)
        for day in self.data['week']:
            day_ingredients = self.get_ingredients_for_day(day, api)
            for ingredient in day_ingredients:
                key = (ingredient['ingredient'], ingredient['unit'])
                weekly_ingredient_aggregator[key] += ingredient['amount']
        aggregated_ingredients = [{'amount': amt, 'unit': unit, 'ingredient': name} for (name, unit), amt in weekly_ingredient_aggregator.items()]

        return aggregated_ingredients
    
    def get_nutrients_for_week(self):
        week_nutrients = {'calories': 0, 'protein': 0, 'fat': 0, 'carbohydrates': 0}
        for day in self.data['week']:
            day_nutrients = self.get_nutrient_info(day)
            for nutrient, amount in day_nutrients.items():
                week_nutrients[nutrient] += amount
        return week_nutrients

class Meal:
    def __init__(self, id, title, ingredients):
        self.id = id
        self.title = title
        self.ingredients = ingredients

    def __str__(self):
        return f"{self.title} (ID: {self.id}): Ingredients - {', '.join(self.ingredients)}"
