from api.spoonacular import SpoonacularAPI as sp

class MealPlan:
    def __init__(self, data):
        self.data = data

    def get_day_meal_ids(self, day):
        return [meal['id'] for meal in self.data['week'][day]['meals']]

    def get_day_meals(self, day):
        return self.data['week'][day]['meals']

    def get_nutrient_info(self, day):
        return self.data['week'][day]['nutrients']
    
    def get_ingredients_for_day(self, day, api):
        from collections import defaultdict
        ingredient_aggregator = defaultdict(float)
        
        meal_ids = self.get_day_meal_ids(day)
        for meal_id in meal_ids:
            recipe_info = api.get_recipe_information(meal_id)
            if recipe_info and 'extendedIngredients' in recipe_info:
                for item in recipe_info['extendedIngredients']:
                    key = (item['name'], item.get('unit', ''))
                    ingredient_aggregator[key] += item.get('amount', 0)
        
        # Converting to a list of tuples for easier table display
        aggregated_ingredients = [{'amount': amt, 'unit': unit, 'ingredient': name} for (name, unit), amt in ingredient_aggregator.items()]
        return aggregated_ingredients
    
    def get_ingredients_for_week(self, api):
        from collections import defaultdict
        weekly_ingredient_aggregator = defaultdict(float)

        for day in self.data['week']:
            meal_ids = self.get_day_meal_ids(day)
            for meal_id in meal_ids:
                recipe_info = api.get_recipe_information(meal_id)
                if recipe_info and 'extendedIngredients' in recipe_info:
                    for item in recipe_info['extendedIngredients']:
                        key = (item['name'], item.get('unit', ''))
                        weekly_ingredient_aggregator[key] += item.get('amount', 0)
        
        # Converting to a list of dictionaries for easier table display
        aggregated_ingredients = [{'amount': amt, 'unit': unit, 'ingredient': name} for (name, unit), amt in weekly_ingredient_aggregator.items()]
        return aggregated_ingredients

class Meal:
    def __init__(self, id, title, ingredients):
        self.id = id
        self.title = title
        self.ingredients = ingredients

    def __str__(self):
        return f"{self.title} (ID: {self.id}): Ingredients - {', '.join(self.ingredients)}"
