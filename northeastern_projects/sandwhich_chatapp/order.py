"""
contains class object with attributes and methods for adding sandwiches to customer order, printing and confirming order contents
"""

import sandwich, menu

class Order:
    def __init__(self):
        self.wichList = []
        self.orderComplete = False
        self.breadCheck = False
        self.spreadCheck = False
        self.numItems = 0
        self.orderState = "default"
        # self.previousSate = ""

    def buildSandwich(self, menuMatch):
        menuItemFound = menu.sandwichDf[menu.sandwichDf["name"] == menuMatch][["name", "bread", "dressing", "meat", "cheese", "veggie"]]
        name, bread, dressing, meat, cheese, veggie = menuItemFound.name.iloc[0], menuItemFound.bread.iloc[0], \
                                                    menuItemFound.dressing.iloc[0], menuItemFound.meat.iloc[0], \
                                                    menuItemFound.cheese.iloc[0], menuItemFound.veggie.iloc[0]
        mySandwich = sandwich.Sandwich(name, bread, dressing, meat, cheese, veggie)
        self.wichList.append(mySandwich)
        self.numItems += 1

    def printOrder(self):
        print(f"Server: So, you have ordered {self.numItems} item(s) so far.  Here is what I have written down:")
        for thisWich in self.wichList:
            thisName = thisWich.name
            thisBread = Order.getIngredientString(thisWich.bread)
            dressings = Order.getIngredientString(thisWich.dressing)
            meats = Order.getIngredientString(thisWich.meat)
            cheeses = Order.getIngredientString(thisWich.cheese)
            veggies = Order.getIngredientString(thisWich.veggie)
            
            responseRoot = f"Server: Your {thisName} comes with"
            orderOut = responseRoot
            
            if len(meats) > 0:
                orderOut = orderOut + " " + meats
            if len(cheeses) > 0:
                orderOut = orderOut + " " + cheeses + " cheese "
            if len(veggies) > 0:
                orderOut = orderOut + " " + veggies

            orderOut = orderOut + " dressed with " + dressings + " on " + thisBread
            orderOut = orderOut.replace("  ", " ")

            print(orderOut)

    @staticmethod
    def getIngredientString(ingredientList):
        if len(ingredientList) == 1:
            return ingredientList[0]
        elif len(ingredientList) == 0:
            return ""
        return " ".join(ingredientList[:-1]) + " and " + ingredientList[-1]