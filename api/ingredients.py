import csv
import os

class IngredientNames:
    # Class attributes to cache the ingredient names and IDs after loading them once.
    _ingredient_names = None
    _ingredient_ids = None

    @classmethod
    def get_ingredient_names(cls):
        # If the list of ingredient names is not already cached, read them from a CSV file.
        if cls._ingredient_names is None:
            # Construct the file path for ingredients.csv located in the same directory as this script.
            filename = os.path.join(os.path.dirname(__file__), 'ingredients.csv')
            with open(filename, 'r') as file:  # Open the file for reading.
                reader = csv.reader(file, delimiter=';')  # Create a CSV reader object.
                cls._ingredient_names = []  # Initialize the list to store ingredient names.
                cls._ingredient_ids = []  # Initialize the list to store ingredient IDs.
                for row in reader:
                    # Append the ingredient name from the first column in each row to the list.
                    cls._ingredient_names.append(row[0])
                    # Append the ingredient ID from the second column in each row to the list.
                    cls._ingredient_ids.append(row[1])
        # Return the list of ingredient names.
        return cls._ingredient_names

    @classmethod
    def get_ingredient_ids(cls):
        # If the list of ingredient IDs is not already cached, call get_ingredient_names to load them.
        if cls._ingredient_ids is None:
            cls.get_ingredient_names()  # Populate both _ingredient_names and _ingredient_ids.
        # Return the list of ingredient IDs.
        return cls._ingredient_ids


# Code below is executed only when the script is run directly, not when imported as a module.
if __name__ == '__main__':
    # Get and print the list of ingredient names to verify that they are loaded correctly.
    ingredient_names = IngredientNames.get_ingredient_names()
    print(ingredient_names)
