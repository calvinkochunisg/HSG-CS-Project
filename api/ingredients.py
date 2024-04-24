import csv
import os

class IngredientNames:
    _ingredient_names = None
    _ingredient_ids = None

    @classmethod
    def get_ingredient_names(cls):
        if cls._ingredient_names is None:
            filename = os.path.join(os.path.dirname(__file__), 'ingredients.csv')
            with open(filename, 'r') as file:
                reader = csv.reader(file, delimiter=';')
                cls._ingredient_names = []
                cls._ingredient_ids = []
                for row in reader:
                    cls._ingredient_names.append(row[0])  # Change row[0] to the correct index if necessary
                    cls._ingredient_ids.append(row[1])  # Change row[1] to the correct index if necessary
        return cls._ingredient_names

    @classmethod
    def get_ingredient_ids(cls):
        if cls._ingredient_ids is None:
            cls.get_ingredient_names()  # This will populate both _ingredient_names and _ingredient_ids
        return cls._ingredient_ids


if __name__ == '__main__':
    ingredient_names = IngredientNames.get_ingredient_names()
    print(ingredient_names)