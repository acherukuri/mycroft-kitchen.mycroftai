from mycroft.skills.core import MycroftSkill
from mycroft.util.log import getLogger
from mycroft import intent_file_handler

LOGGER = getLogger(__name__)

class KitchenSkill(MycroftSkill):
    def __init__(self):
        super(KitchenSkill, self).__init__(name="KitchenSkill")
    
    def get_recipe_for_dish(self, message):
        dish = message.data.get('dish')
        data = {"dish": dish}
        self.log.info('dish name is: ' + dish)
        self.speak_dialog("recipe", data)

    @intent_file_handler("recipe.ingredients.intent")
    def handle_recipe_ingredients_intent(self, message):
        self.get_recipe_for_dish(message)

    def stop(self):
        pass


def create_skill():
    return KitchenSkill()
