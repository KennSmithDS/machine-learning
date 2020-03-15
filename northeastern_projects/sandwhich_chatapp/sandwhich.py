# Importing Python libraries used to create sandwhich shop bot
import re, sys, os, logging
import random, string
from collections import OrderedDict
from collections import Counter
import pandas as pd
import datetime as dt
import menu, langref

currentDt = dt.datetime.now().strftime('%m-%d-%Y-%H%M%S')
logPath = os.path.join(os.getcwd(), 'logs')

if not os.path.exists(logPath):
    os.mkdir(logPath)

# fileName = os.path.join(logPath, f'sandwhichshop__{currentDt}.log')
# logging.basicConfig(filename=fileName,level=logging.DEBUG)

""" 

NOTE: We are explicitly not allowed to use libraries like NLTK, Gensim, SciKit, or spaCy on this assignment
"""

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
        self.positives = ["no", "nope", "incorrect", "wrong"]
        self.negatives = ["bingo", "yay", "yes", "yeah", "absolutely", "correct", "yup"]
        self.lastInstructions = []
        self.ngrams = []

    def listenToCustomer(self, attentionSpan):
        userInput = input()
        cleanUserInput = ShopBot.cleanInput(userInput)
        self.lastInstructions.append(cleanUserInput)
        ngramTuple = self.getNgrams(cleanUserInput.split(), attentionSpan)
        ngramList = [ngram for ngram in ngramTuple]
        self.ngrams.append(ngramList)

    def confirmResponse(self, response):
        cleanResponse = ShopBot.cleanInput(response)
        for pos in self.positives:
            if cleanResponse.find(pos) != -1:
                return True
        return False

    # Function that takes token list of strings and creates custom length n-grams
    def getNgrams(self, tokens, n=3):
        nowNgrams = []
        for idx in range(len(tokens)-n+1):
            yield tuple(tokens[idx:idx+n])

    def menuDialogue(self, menub):
        print(random.choice(self.confirmations))
        menub.readMenu()
        menub.menuRead = True
        print(random.choice(self.openings))
        self.listenToCustomer(3)

    def orderDialogue(self):
        for ngram in self.ngrams[-1]:
            # print(ngram)
            ngramString = " ".join(ngram)
            # print(ngramString)
            for sammy in menu.sandwhichDf['name'].unique():
                if self.editDist(ngramString, sammy, len(ngramString), len(sammy)) <= .3:
                    print(f'You would like the {sammy}, correct?')
                    response = input()
                    if self.confirmResponse(response):
                else:
                    print("I'm terribly sorry I don't think we make that sandwhich here.  Is there something else I can get you?")
                    self.listenToCustomer(3)
                    self.orderDialogue()

    # Function to take user input(), remove special characters, stop words, and make all lower case
    @staticmethod
    def cleanInput(inputString):
        alphanumInput = re.sub(r"[^A-Za-z0-9 ]+", "", inputString)
        lowerSingularNoStops = [langref.makeSingular(word.lower()) for word in alphanumInput.split() if word.lower() not in langref.stopWords]
        outputString = " ".join(lowerSingularNoStops)
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
        
        # print(inputString, ingredientString)
        # print(dpTable[m][n] / n)
        return float(dpTable[m][n] / n)

    # Salutation when the customer enters or exits the shop
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
    todaysMenu = menu.Menu(menu.sandwhichDf, menu.ingredientDf)
    openingGreeting = random.choice(shopBot.greetings) + ", " + random.choice(shopBot.openings)
    print(openingGreeting)
    shopBot.listenToCustomer(3)

    customerOrder = Order()
    while(customerOrder.orderComplete == False):

        for ngram in shopBot.ngrams[-1]:
            if ("menu" in ngram or "option" in ngram or "list" in ngram or "special" in ngram) and todaysMenu.menuRead == False:
                shopBot.menuDialogue(todaysMenu)
                shopBot.orderDialogue()
            else:
                shopBot.orderDialogue()

        customerOrder.orderComplete = True

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

