import requests
import streamlit as st

class SpoonacularAPI:
    """
    A class used to interact with the Spoonacular API.
    ...
    API Documentation
    ----------
    See Link: https://spoonacular.com/food-api/docs

    Attributes
    ----------
    _VALID_DIETS : list
        A list of valid diets that can be used with the Spoonacular API. Will not change.
    _BASE_URL : str
        The base URL for the Spoonacular API. Will not change.
    _api_key : str
        The API key for the Spoonacular API.
    diet : str
        The diet to use when generating meal plans. Must be one of the valid diets.

    Methods
    -------
    validate_diet(diet)
        Validates that the given diet is one of the valid diets.
    construct_url(endpoint, params=None)
        Constructs a URL for the given endpoint and query parameters.
    generate_meal_plan(timeframe=None, targetCalories=None, diet=None, exclude=[])
        Generates a meal plan using the Spoonacular API.
    """
    def __init__(self, diet = None) -> None:
        """
        Constructs a new SpoonacularAPI object.

        Parameters
        ----------
        diet : str, optional
            The diet to use when generating meal plans. Must be one of the valid diets.
        """
        # Constants
        self._BASE_URL = "https://api.spoonacular.com/" # Secrets are stored in the .streamlit/secrets.toml file
        self._VALID_DIETS = ["gluten_free", "ketogenic", "vegetarian", "lacto-vegetarian", "ovo-vegetarian", "vegan", "pescetarian", "paleo", "primal", "low_fodmap", "whole30"]
        self._API_KEY = "4deaceca7a6448ba9d2006710177aad3" # Secrets are stored in the .streamlit/secrets.toml file

        # Attributes
        self.diet = diet # This will call the setter method below see @diet.setter
    
    @property
    def diet(self) -> str:
        """The diet to use when generating meal plans. Must be one of the valid diets."""
        return self._diet
    
    @diet.setter
    def diet(self, diet) -> None:
        """Sets the diet attribute, validating that it's one of the valid diets."""
        self._diet = self.validate_diet(diet) # runs the validate_diet method below

    def validate_diet(self, diet) -> str:
        """
        Validates that the given diet is one of the valid diets.

        Parameters
        ----------
        diet : str
            The diet to validate.

        Returns
        -------
        str
            The validated diet.

        Raises
        ------
        ValueError
            If the diet is not one of the valid diets.
        """
        if diet is not None and diet not in self._VALID_DIETS: # valid diets are defined in the __init__ method
            raise ValueError(f"Invalid diet: {diet}. Valid options are: {', '.join(self._VALID_DIETS)}")
        return diet



    def construct_url(self, endpoint, params = None) -> str:
        """
        Constructs a URL for the given endpoint and query parameters.

        Parameters
        ----------
        endpoint : str
            The API endpoint to construct the URL for. Must start with a lowercase letter.
        params : dict, optional
            A dictionary of query parameters to include in the URL.

        Returns
        -------
        str
            The constructed URL.
        """
        url = f"{self._BASE_URL}{endpoint}" # Base URL is defined in the __init__ method
        if params:
            query_string = "&".join(f"{key}={value}" for key, value in params.items()) # Convert the params dict to a query string separated by "&"
            url = f"{url}?{query_string}" # Append the query string to the URL
        return url



    def generate_meal_plan(self, timeframe = None, targetCalories = None, diet = None, exclude = [] ) -> None:
        """
        Generates a meal plan using the Spoonacular API.

        Parameters
        ----------
        timeframe : str, optional
            The timeframe to generate the meal plan for. Must be either "day" or "week". Defaults to "week".
        targetCalories : int, optional
            The target number of calories for the meal plan. Must be a positive integer.
        diet : str, optional
            The diet to use when generating the meal plan. Must be one of the valid diets.
        exclude : list, optional
            A list of ingredients to exclude from the meal plan.

        Returns
        -------
        json
            The generated meal plan.

        Raises
        ------
        requests.RequestException
            If an error occurs while making the request to the Spoonacular API.
        """
        # The endpoint for the generate meal plan API (Tells the API what to do)
        endpoint = "mealplanner/generate"

        # Checks if the parameters are valid and sets them to None if they are not
        # TODO: Add error handling here to raise errors when a parameter is wrong
        params = {
                    "apiKey": self._API_KEY,
                    "timeframe": timeframe if timeframe in ["day", "week"] else "week",
                    "targetCalories": targetCalories if type(targetCalories) == int and targetCalories > 0 else None,
                    "diet": self.validate_diet(diet),
                    "exclude": ",".join(exclude) if exclude else None
                  }
        
        # Remove keys with None values
        params = {k: v for k, v in params.items() if v is not None}
        
        # Construct the URL
        url = self.construct_url(endpoint, params)

        # Make the request to the API and raise an error if it fails
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises a HTTPError if the response was an error
        except requests.RequestException as e:
            print(f"An error occurred while making the request: {e}")
            return None

        # Save the response as a json object in data
        data = response.json()

        # TODO: Process Data here. Structure data and return it in a nice way for UI

        return url




"""
Here the module can be testet, the following code will not be excecuted when importing the module somwhere else.

See Documentation of " if __name__ == "__main__": " here: https://realpython.com/if-name-main-python/
"""
if __name__ == "__main__":
    sp = SpoonacularAPI()
    print(sp.generate_meal_plan(diet = "vegetarian"))