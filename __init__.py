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
            self.speak_dialog("recipe", data)

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
        recipe = message.data.get('recipe')
        lookup_recipe = {"recipe": recipe}
        self.speak_dialog("looking.up.recipe.instructions.now", lookup_recipe)

    @intent_file_handler("cook.make.prepare.intent")
    def handle_prepare_recipe_intent(self, message):
        self.get_instructions_for_recipe(message)

    def stop(self):
        pass

def create_skill():
    return KitchenSkill()
