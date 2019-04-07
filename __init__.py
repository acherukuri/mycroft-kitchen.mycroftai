import requests
from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft import intent_file_handler, intent_handler
from adapt.intent import IntentBuilder

LOGGER = getLogger(__name__)

class KitchenSkill(MycroftSkill):
    def __init__(self):
        super(KitchenSkill, self).__init__(name="KitchenSkill")
        self.recipe_search_url = "https://api.edamam.com/search?q={}&app_id=45d96e9b&app_key=340e6e97add2df98e6d6dd76c52efa19&from=0&to=1"
    
    def get_recipe_for_dish(self, message):
        dish = message.data.get('dish')
        lookup_dish = {"dish": dish}
        self.speak_dialog("looking.up.recipe.now", lookup_dish)
        resp = requests.get(self.recipe_search_url.format(dish))
        if resp.status_code != 200:
            self.speak_dialog("error.occurred")
            return None
        elif resp.status_code == 200:
            resp = resp.json()
            recipe = resp['hits'][0]['recipe'] # TODO: handle empty recipe response
            data = {"dish": dish, "source": recipe['source'],
                    "ingredients": ', '.join(recipe['ingredientLines'])}
            self.speak_dialog("recipe.ingredients", data)

    @intent_file_handler("recipe.ingredients.intent")
    def handle_recipe_ingredients_intent(self, message):
        self.get_recipe_for_dish(message)

    # def get_recipe_by_ingredients(self, message):
    #     self.speak_dialog("looking.up.dish.now", expect_response = True)

    # @intent_handler(IntentBuilder('IngredientsToRecipeIntent')
    #                 .require('Question'))
    # def handle_ingredients_to_recipe_intent(self, message):
    #     self.get_recipe_by_ingredients(message)

    def get_instructions_for_recipe(self, message):
        rapidapi_request_headers = {"X-RapidAPI-Host": "spoonacular-recipe-food-nutrition-v1.p.rapidapi.com",
                                    "X-RapidAPI-Key": "7901ed752fmshba3efc948722d09p158bc6jsn67dc2908cbf8"}
        find_recipe_id_url = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/search?query={}'
        find_recipe_instructions_url = 'https://spoonacular-recipe-food-nutrition-v1.p.rapidapi.com/recipes/{}/information'
        recipe = message.data.get('recipe')
        lookup_recipe = {"recipe": recipe}
        self.speak_dialog("looking.up.instructions.now", lookup_recipe)
        recipe_id_resp = requests.get(find_recipe_id_url.format(recipe),
                                      headers = rapidapi_request_headers)
        if recipe_id_resp.status_code != 200:
            self.speak_dialog("error.occurred")
            return None
        elif recipe_id_resp.status_code == 200:
            recipe_id_results = recipe_id_resp.json()
            recipe_id = recipe_id_results['results'][0]['id'] # TODO: handle empty recipe response
            recipe_instructions_resp = requests.get(find_recipe_instructions_url.format(recipe_id),
                                                    headers = rapidapi_request_headers)
            if recipe_instructions_resp.status_code != 200:
                self.speak_dialog("error.occurred")
                return None
            elif recipe_instructions_resp.status_code == 200:
                recipe_instructions_result = recipe_instructions_resp.json()
                source = recipe_instructions_result['sourceName']
                instructions = recipe_instructions_result['instructions']
                data = {"instructions": instructions, "source": source,
                        "recipe": recipe}
                self.speak_dialog("recipe.instructions", data)

    @intent_file_handler("cook.make.prepare.intent")
    def handle_prepare_recipe_intent(self, message):
        self.get_instructions_for_recipe(message)

    def stop(self):
        pass

def create_skill():
    return KitchenSkill()
