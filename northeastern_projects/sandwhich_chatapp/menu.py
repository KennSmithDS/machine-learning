"""
contins class object with attributes and methods for containing and reading off the menu options
"""

import pandas as pd
import os

class Menu:
    def __init__(self, sandwiches, ingredients):
        self.sandwiches = sandwiches
        self.ingredients = ingredients
        self.menuLength = len(self.sandwiches)
        self.menuRead = False

    def readMenu(self):

        print("-"*100)
        print('Server: ', f"These are our {self.menuLength} specials today:")

        for i in range(self.menuLength):
            thisWich = self.sandwiches.iloc[i]
            thisName = thisWich["name"]
            thisBread = thisWich["bread"][0]
            dressings = Menu.getIngredientString(thisWich["dressing"])
            meats = Menu.getIngredientString(thisWich["meat"])
            cheeses = Menu.getIngredientString(thisWich["cheese"])
            veggies = Menu.getIngredientString(thisWich["veggie"])
            
            responseRoot = f"{i+1}) {thisName} comes with"
            menuOut = responseRoot
            
            if len(meats) > 0:
                menuOut = menuOut + " " + meats
            if len(cheeses) > 0:
                menuOut = menuOut + " " + cheeses + " cheese "
            if len(veggies) > 0:
                menuOut = menuOut + " " + veggies

            menuOut = menuOut + " dressed with " + dressings + " on " + thisBread
            menuOut = menuOut.replace("  ", " ")

            print(menuOut)

        print("-"*100)

    def readOptions(self, ingredientType):
        print('Server: ', f"Your {ingredientType} options are:")
        ingredientSet = list(self.ingredients[self.ingredients["type"]==ingredientType]["ingredient"].values)
        for item in ingredientSet:
            print(" - ", item)

    @staticmethod
    def getIngredientString(ingredientList):
        if len(ingredientList) == 1:
            return ingredientList[0]
        elif len(ingredientList) == 0:
            return ""
        return " ".join(ingredientList[:-1]) + " and " + ingredientList[-1]

wichDictList = [
    {"name": "kendalls sour club", "bread": ["sourdough"], "dressing": ["mustard","thousand island","ranch","vinegar"], "cheese": ["camembert"], "meat": ["spam"], "veggie": ["onion","saeurkraut","pickle","sriracha"]},
    {"name": "classic turkey club", "bread": ["white"], "dressing": ["mayo"], "cheese": ["pepper jack"], "meat": ["turkey","bacon"], "veggie": ["tomato","lettuce"]},
    {"name": "italian club", "bread": ["white"], "dressing": ["mayo","olive oil","vinegar"], "cheese": ["provolone"], "meat": ["ham","salami"], "veggie": ["onion","lettuce","tomato","peperoncino"]},
    {"name": "beach club", "bread": ["white"], "dressing": ["mayo"], "cheese": ["provolone"], "meat": ["tuna"], "veggie": ["lettuce","tomato","cucumber","avocado"]},
    {"name": "veggie club", "bread": ["wheat"], "dressing": ["vinegar"], "cheese": [], "meat": [], "veggie": ["hummus","onion","lettuce","tomato","cucumber","avocado","bell pepper"]},
    {"name": "grilled cheese", "bread": ["white"], "dressing": ["mayo"], "cheese": ["american"], "meat": [], "veggie": []},
    {"name": "classic reuben", "bread": ["rye"], "dressing": ["thousand island"], "cheese": ["swiss"], "meat": ["beef"], "veggie": ["saeurkraut"]},
    {"name": "grilled peanut butter jelly bacon", "bread":["white"], "dressing": ["peanut butter","jelly"], "cheese": [], "meat":["bacon"], "veggie":[]}]
sandwichDf = pd.DataFrame(wichDictList)
# print(sandwichDf.head())

ingredDictList = [
    {"ingredient": "lettuce", "type": "bread"},{"ingredient": "white", "type": "bread"},{"ingredient": "wheat", "type": "bread"},
    {"ingredient": "rye", "type": "bread"},{"ingredient": "olive oil", "type": "dressing"},{"ingredient": "vinegar", "type": "dressing"},
    {"ingredient": "ranch", "type": "dressing"},{"ingredient": "mayo", "type": "dressing"},{"ingredient": "mustard", "type": "dressing"},
    {"ingredient": "thousand island", "type": "dressing"},{"ingredient": "salt", "type": "dressing"},{"ingredient": "pepper", "type": "dressing"},
    {"ingredient": "peanut butter", "type": "dressing"},{"ingredient": "jelly", "type": "dressing"},{"ingredient": "bacon", "type": "meat"},
    {"ingredient": "spam", "type": "meat"},{"ingredient": "beef", "type": "meat"},{"ingredient": "turkey", "type": "meat"},{"ingredient":"sriracha", "type": "dressing"},
    {"ingredient": "tuna", "type": "meat"},{"ingredient": "ham", "type": "meat"},{"ingredient": "salami", "type": "meat"},{"ingredient": "french", "type": "bread"},
    {"ingredient": "chicken", "type": "meat"},{"ingredient": "provolone", "type": "cheese"},{"ingredient": "camembert", "type": "cheese"},
    {"ingredient": "swiss", "type": "cheese"},{"ingredient": "american", "type": "cheese"},{"ingredient": "cheddar", "type": "cheese"},
    {"ingredient": "pepper jack", "type": "cheese"},{"ingredient": "saeurkraut", "type": "veggie"},{"ingredient": "lettuce", "type": "veggie"},
    {"ingredient": "tomato", "type": "veggie"},{"ingredient": "cucumber", "type": "veggie"},{"ingredient": "avocado", "type": "veggie"},
    {"ingredient": "onion", "type": "veggie"},{"ingredient": "olive", "type": "veggie"},{"ingredient": "bell pepper", "type": "veggie"},
    {"ingredient": "peperoncino", "type": "veggie"},{"ingredient": "pickle", "type": "veggie"}, {"ingredient": "sourdough", "type": "bread"}]
ingredientDf = pd.DataFrame(ingredDictList)
# print(ingredientDf.head())