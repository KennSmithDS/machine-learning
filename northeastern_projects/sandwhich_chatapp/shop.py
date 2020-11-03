# Importing Python libraries used to create sandwich shop bot
import re, sys, os, logging, time
import random, string, webbrowser
from collections import OrderedDict
from collections import Counter
import pandas as pd
import datetime as dt
import menu, langref, chatbot, order, sandwich

currentDt = dt.datetime.now().strftime("%m-%d-%Y-%H%M%S")
logPath = os.path.join(os.getcwd(), "logs")

if not os.path.exists(logPath):
    os.mkdir(logPath)

# commented out because logging all statements doesn't allow customer to see responses :-)
# will come back later to modify so some conversation components are written to log file
# fileName = os.path.join(logPath, f"sandwichshop__{currentDt}.log")
# logging.basicConfig(filename=fileName,level=logging.DEBUG)

""" 
primary application file that drives the state machine and makes successive calls to class methods
We are explicitly not allowed to use libraries like NLTK, Gensim, SciKit, or spaCy on this assignment
"""

if __name__ == "__main__":
    
    shopBot = chatbot.ShopBot()
    shopBot.shopSalutation("WELCOME TO KENDALLS SANDWICH SHOP ", 32)
    openingGreeting = random.choice(shopBot.greetings) + ", " + random.choice(shopBot.openings)
    print('Server: ', openingGreeting)

    todaysMenu = menu.Menu(menu.sandwichDf, menu.ingredientDf)
    customerOrder = order.Order()
    loopCounter = 0

    while(customerOrder.orderComplete == False):
        
        # print(f"Order State: {customerOrder.orderState}")
        # print(f"Cycle: {loopCounter}")
        
        if loopCounter == 0:
            shopBot.listenToCustomer()
            print('Server: ', random.choice(shopBot.confirmations))
            customerOrder.orderState = "IdentifySandwich"
            loopCounter += 1

        if ("choice" in shopBot.lastInstructions[-1].split() or "choices" in shopBot.lastInstructions[-1].split() or "menu" in shopBot.lastInstructions[-1].split() or "option" in shopBot.lastInstructions[-1].split() or "list" in shopBot.lastInstructions[-1].split() or "special" in shopBot.lastInstructions[-1].split()):
            for ingredient in ["bread", "meat", "cheese", "dressing", "veggie"]:
                if ingredient in shopBot.lastInstructions[-1].split():
                    todaysMenu.readOptions(ingredient)

            shopBot.menuDialogue(todaysMenu)
            shopBot.listenToCustomer()
            print('Server: ', random.choice(shopBot.confirmations))
            
            if customerOrder.numItems == 0:
                customerOrder.orderState = "IdentifySandwich"
            else:
                customerOrder.orderState = "MakeChanges"

        if customerOrder.orderState == "IdentifySandwich":

            sammyFound, exceptFound = shopBot.orderDialogue()
            # print(sammyFound, exceptFound)

            if sammyFound is not None:
                customerOrder.buildSandwich(sammyFound)
                if len(exceptFound) > 0:
                    shopBot.exceptionQueue = chatbot.Queue()
                    for excpt in exceptFound:
                        shopBot.exceptionQueue.push(excpt)
                    customerOrder.orderState = "MakeChanges"
                else:
                    customerOrder.orderState = "ConfirmOrder"

            else:
                shopBot.listenToCustomer()
                for word in shopBot.lastInstructions[-1].split():
                    if word in shopBot.negatives:
                        customerOrder.orderState = 'ExitShop'
                    else:
                        customerOrder.orderState = 'default'
                    break

        elif customerOrder.orderState == "MakeChanges":

            while not shopBot.exceptionQueue.isEmpty():
                excpt = shopBot.exceptionQueue.pop()
                requestType = excpt[0]
                ingredientName = excpt[1]
                if ingredientName not in menu.ingredientDf['ingredient'].unique().tolist():
                    pass
                else:
                    # print(requestType, ingredientName)
                    ingredientType = menu.ingredientDf[menu.ingredientDf['ingredient']==ingredientName]['type'].iloc[0]
                    if requestType in langref.exceptionWords:
                        customerOrder.wichList[-1].makeException(ingredientType, ingredientName)
                    elif requestType in langref.additionWords:
                        customerOrder.wichList[-1].makeAddition(ingredientType, ingredientName)
                    elif requestType in langref.substitutionWords:
                        if len(excpt) == 4:
                            ingredientName2 = excpt[3]
                            ingredientType2 = menu.ingredientDf[menu.ingredientDf['ingredient']==ingredientName2]['type'].iloc[0]
                            customerOrder.wichList[-1].makeAddition(ingredientType2, ingredientName2)
                            customerOrder.wichList[-1].makeException(ingredientType, ingredientName)
                        else:
                            print("Server: I'm sorry, we don't make those kind of substitutions here")
            customerOrder.orderState = "ConfirmOrder"
        
        elif customerOrder.orderState == "ConfirmOrder":

            if len(customerOrder.wichList) == 0:
                customerOrder.orderState = 'ExitShop'

            customerSandwich = customerOrder.wichList[-1]

            # bread check
            while customerOrder.breadCheck == False:
                defaultBread = menu.sandwichDf[menu.sandwichDf['name']==customerSandwich.name]['bread'].iloc[0]
                breadString = order.Order.getIngredientString(defaultBread)
                print(f"What kind of bread would you like?  The {customerSandwich.name} usually comes with {breadString}")
                shopBot.listenToCustomer()

                if ("choice" in shopBot.lastInstructions[-1].split() or "menu" in shopBot.lastInstructions[-1].split() or "option" in shopBot.lastInstructions[-1].split() or "list" in shopBot.lastInstructions[-1].split() or "special" in shopBot.lastInstructions[-1].split()):
                    todaysMenu.readOptions('bread')
                    shopBot.listenToCustomer()
                
                if ("default" in shopBot.lastInstructions[-1].split() or "regular" in shopBot.lastInstructions[-1].split() or "regularly" in shopBot.lastInstructions[-1].split() or "normal" in shopBot.lastInstructions[-1].split() or "normally" in shopBot.lastInstructions[-1].split() or "usual"  in shopBot.lastInstructions[-1].split() or "usually"  in shopBot.lastInstructions[-1].split() or "fine" in shopBot.lastInstructions[-1].split() or "good" in shopBot.lastInstructions[-1].split() or "great" in shopBot.lastInstructions[-1].split()):
                    pass

                else:

                    sandwichBread = customerSandwich.bread
                    breadRequest = shopBot.lastInstructions[-1].split()
                    overage = [bread for bread in sandwichBread if bread not in breadRequest]

                    for word in breadRequest:
                        if word not in sandwichBread:
                            if word in menu.ingredientDf['ingredient'].unique().tolist():
                                customerSandwich.makeAddition('bread', shopBot.lastInstructions[-1])
                            else:
                                print(f"Server: I'm sorry but we don't have {word}")

                    for item in overage:
                        customerSandwich.makeException('bread', item)

                customerOrder.breadCheck = True

            # dressing check
            while customerOrder.spreadCheck == False:
                defaultSpread = menu.sandwichDf[menu.sandwichDf['name']==customerSandwich.name]['dressing'].iloc[0]
                spreadString = order.Order.getIngredientString(defaultSpread)
                print(f"What kind of spread/dressing would you like? {customerSandwich.name} usually comes with {spreadString}")
                shopBot.listenToCustomer()

                if ("choice" in shopBot.lastInstructions[-1].split() or "choices" in shopBot.lastInstructions[-1].split() or "menu" in shopBot.lastInstructions[-1].split() or "option" in shopBot.lastInstructions[-1].split() or "list" in shopBot.lastInstructions[-1].split() or "special" in shopBot.lastInstructions[-1].split()):
                    todaysMenu.readOptions('dressing')
                    shopBot.listenToCustomer()

                if ("default" in shopBot.lastInstructions[-1].split() or "regular" in shopBot.lastInstructions[-1].split() or "regularly" in shopBot.lastInstructions[-1].split() or "normal" in shopBot.lastInstructions[-1].split() or "normally" in shopBot.lastInstructions[-1].split() or "usual"  in shopBot.lastInstructions[-1].split() or "usually"  in shopBot.lastInstructions[-1].split() or "fine" in shopBot.lastInstructions[-1].split() or "good" in shopBot.lastInstructions[-1].split() or "great" in shopBot.lastInstructions[-1].split()):
                    pass

                else:

                    sandwichSpread = customerSandwich.dressing
                    spreadRequest = shopBot.lastInstructions[-1].split()
                    overage = [spread for spread in sandwichSpread if spread not in spreadRequest]
                    
                    for word in spreadRequest:
                        if word not in sandwichSpread:
                            if word in menu.ingredientDf['ingredient'].unique().tolist():
                                customerSandwich.makeAddition('dressing', shopBot.lastInstructions[-1])
                            else:
                                print(f"Server: I'm sorry but we don't have {word}")

                    for item in overage:
                        customerSandwich.makeException('dressing', item)

                customerOrder.spreadCheck = True
            
            print("Server: I would like to confirm your order...")
            customerOrder.printOrder()

            print("Server: Does that sound about right?")
            orderConfirmation = input()

            if shopBot.confirmResponse(orderConfirmation):

                print("Server: Give me a minute while I make that for you!\n")
                shopBot.shopSalutation("MUSIC BEGINS TO PLAY IN THE BACKGROUND", 30)
                if customerSandwich.name == "grilled peanut butter jelly bacon":
                    waitUrl = 'https://www.youtube.com/watch?v=s8MDNFaGfT4'
                else:
                    waitUrl = 'https://www.youtube.com/watch?v=wUDqQSwdBjM'
                webbrowser.open_new(waitUrl)
                time.sleep(30)

                print("Server: Here's your sandwich!")
                customerOrder.wichList[-1].showSandwich()
                customerOrder.orderComplete = True
                
            else:
                
                customerOrder.orderState = "IdentifySandwich"
                print("Server: I'm sorry about that, could you please repeat your order?")
                customerOrder.wichList = []
                shopBot.listenToCustomer()

        else:

            print("Server: I'm sorry we couldn't be of more assistance to you today, take care")
            customerOrder.orderComplete = True

    shopBot.shopSalutation("THANKS FOR SHOPPING AT KENDALLS SANDWICH SHOP ", 26)
