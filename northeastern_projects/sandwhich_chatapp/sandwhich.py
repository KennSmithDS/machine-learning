# Importing Python libraries used to create sandwhich shop bot
import re, sys, os, logging
import random, string
from collections import OrderedDict
from collections import Counter
import pandas as pd
import datetime as dt
import menu

currentDt = dt.datetime.now().strftime('%m-%d-%Y-%H%M%S')
logPath = os.path.join(os.getcwd(), 'logs')

if not os.path.exists(logPath):
    os.mkdir(logPath)

# fileName = os.path.join(logPath, f'sandwhichshop__{currentDt}.log')
# logging.basicConfig(filename=fileName,level=logging.DEBUG)

""" 

NOTE: We are explicitly not allowed to use libraries like NLTK, Gensim, SciKit, or spaCy on this assignment
"""

class Menu:
    def __init__(self, sandwhiches, ingredients):
        self.sandwhiches = sandwhiches
        self.ingredients = ingredients
        self.menuLength = len(self.sandwhiches)

    def readMenu(self):

        print("-"*100)
        print(f"These are our {self.menuLength} specials today:")

        for i in range(self.menuLength):
            thisWhich = self.sandwhiches.iloc[i]
            thisName = thisWhich["name"]
            thisBread = thisWhich["bread"][0]
            dressings = Menu.getIngredientString(thisWhich["dressing"])
            meats = Menu.getIngredientString(thisWhich["meat"])
            cheeses = Menu.getIngredientString(thisWhich["cheese"])
            veggies = Menu.getIngredientString(thisWhich["veggie"])
            
            responseRoot = f"{i+1}) {thisName} comes with"
            menuOut = responseRoot
            
            if len(meats) > 0:
                menuOut = menuOut + " " + meats
            if len(cheeses) > 0:
                menuOut = menuOut + " " + cheeses + " cheese "
            if len(veggies) > 0:
                menuOut = menuOut + " " + veggies

            menuOut = menuOut + " dressed with " + dressings + " on " + thisBread
            menuOut = menuOut.replace('  ', ' ')

            print(menuOut)

        print("-"*100)

    def readOptions(self, ingredientType):
        print(f'Your {ingredientType} options are:')
        ingredientSet = list(self.ingredients[self.ingredients['type']==ingredientType]['ingredient'].values)
        for item in ingredientSet:
            print(item)

    @staticmethod
    def getIngredientString(ingredientList):
        if len(ingredientList) == 1:
            return ingredientList[0]
        elif len(ingredientList) == 0:
            return ""
        return " ".join(ingredientList[:-1]) + " and " + ingredientList[-1]

class Sandwhich:
    def __init__(self, name, bread, dressing, meat, cheese, veggie):
        self.name = name
        self.bread = bread
        self.dressing = dressing
        self.meat = meat
        self.cheese = cheese
        self.veggie = veggie

    def makeSubstitution(self):
        pass

    def makeException(self):
        pass

    def makeAddition(self):
        pass

class Order:
    def __init__(self):
        self.whichList = []
        self.orderComplete = False
        self.numItems = 0

    def buildSandwhich(self, menuMatch):
        sandwhich = Sandwhich(menuMatch)
        self.whichList.append(sandwhich)
        self.numItems += 1

    def printOrder(self):
        print(f'So, you have ordered {self.numItems} item(s) so far.  Here is what I have written down:\n')
        for which in self.whichList:
            print(which)

    def confirmOrder(self):
        pass
    
class ShopBot:

    def __init__(self):
        self.greetings = ["hey", "hello", "hi", "howdy", "great to see you", "thanks for coming in today"]
        self.openings = ["whatll it be?", "what can i do ya for?", "what can i get started for you?", "do you know what youd like?"]
        self.confirmations = ["sure thing", "no problem", "coming right up", "you got it", "of course"]
        self.lastInstructions = []
        self.ngrams = []
        self.continueDialogue = True

    def listenToCustomer(self, attentionSpan):
        userInput = input()
        cleanUserInput = ShopBot.cleanInput(userInput)
        self.lastInstructions.append(cleanUserInput)
        ngramTuple = self.getNgrams(cleanUserInput.split(), attentionSpan)
        ngramList = [ngram for ngram in ngramTuple]
        self.ngrams.append(ngramList)

    # Function that takes token list of strings and creates custom length n-grams
    def getNgrams(self, tokens, n=3):
        nowNgrams = []
        for idx in range(len(tokens)-n+1):
            yield tuple(tokens[idx:idx+n])

    # Function to take user input(), remove special characters, stop words, and make all lower case
    @staticmethod
    def cleanInput(inputString):
        alphanumInput = re.sub(r"[^A-Za-z0-9 ]+", "", inputString)
        lowerNoStops = [word.lower() for word in alphanumInput.split() if word.lower() not in menu.stopWords]
        outputString = " ".join(lowerNoStops)
        return outputString

    # Function to take a token string from user input and compute edit distance with each possible ingredient
    @staticmethod
    def editDist(inputString, ingredientString, m, n):
        dpTable = [[0 for x in range(n + 1)] for x in range(m + 1)]

        for i in range(m + 1):
            for j in range(n + 1):
                if i == 0:
                    dpTable[i][j] = j
                elif j == 0:
                    dpTable[i][j] = i
                elif inputString[i-1] == ingredientString[j-1]:
                    dpTable[i][j] = dpTable[i-1][j-1]
                else:
                    dpTable[i][j] = 1 + min(dpTable[i][j-1], dpTable[i-1][j], dpTable[i-1][j-1])
        
        return dpTable[m][n] / n

    # Valediction when the customer enters or exits the shop
    @staticmethod
    def shopSalutation(message, wrapper):
        print("\n")
        print("#"*100)
        salutation = "#"*wrapper + " " + message + " " + "#"*wrapper
        print(salutation)
        print("#"*100)
        print("\n")

if __name__ == "__main__":
    
    shopBot = ShopBot()
    shopBot.shopSalutation("WELCOME TO KENDALLS SANDWHICH SHOP", 32)
    todaysMenu = Menu(menu.sandwhichDf, menu.ingredientDf)
    openingGreeting = random.choice(shopBot.greetings) + ", " + random.choice(shopBot.openings)
    print(openingGreeting)

    while(shopBot.continueDialogue == True):
        shopBot.listenToCustomer(5)
        print(shopBot.lastInstructions[-1])
        print(shopBot.ngrams[-1])
        shopBot.continueDialogue = False

    shopBot.shopSalutation("THANKS FOR SHOPPING AT KENDALLS SANDWHICH SHOP", 26)

    # todaysMenu.readMenu()
    # todaysMenu.readOptions('bread')
    # todaysMenu.readOptions('meat')
    # todaysMenu.readOptions('cheese')
    # todaysMenu.readOptions('veggie')

    # string1 = "hamBurgerZ"
    # string2 = "I love! to eat #hamburgers"
    # string1 = cleanInput(string1)
    # string2 = cleanInput(string2)
    # string2_trigram = getNgrams(string2.split(), n=3)
    # print(string2_trigram)

    # # print(string1, string2)
    # result = editDist(string1, string2, len(string1), len(string2))
    # print(f"The edit distance between '{string1}' and '{string2}' is {result}")

    # edit_perc = (result/len(string2))
    # print("The strings are {0:.0f}% different".format(edit_perc*100))

    # string3 = "I would like kendalls smelly socks but without mustard or onions"
    # string3 = cleanInput(string3)
    # string3_trigram = getNgrams(string3.split(), n=4)
    # print(string3_trigram)

    # ord1 = Order()
    # ord1.buildSandwhich()
    # print(ord1.num_of_items)

    # print(ref.stopWords)

