import re, random
import langref, menu

"""
File contains class definition for the chatbot that users will iterface with when ordering sandwiches

The chatbot has multiple attributes for the different types of expressions it has when interacting, e.g.:
    - greetings, opening statements, confirmations, as well as parsed and cleaned customer input

The chatbot also has various methods to drive customer interaction:
    - listenToCustomer: takes customer input, cleans any cases and non-alphanumeric characters, and parses into clean ngrams for tokenization
    - confirmResponse: checks positive and negative responses to verify a question/request
    - gGrams: dynamically builds a set of ngrams based on input length
    - menuDialogue: reads the menu class from menu.py
    - orderDialogue: dialogue sequence to identify what kind of sandwich, and instantiates sandwich object
    - orderExceptionDialogue: dialogue sequence to identify when customer is making exceptions, additions, replacements
    - orderConfirmationDialogue: dialogue sequence to read order back to customer and confirm correctness
    - editDist: calculates edit distance between two string inputs
"""

class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."

    def __init__(self):
        self.list = []

    def push(self, item):
        "Enqueue the 'item' into the queue"
        self.list.insert(0, item)

    def pop(self):
        """
        Dequeue the earliest enqueued item still in the queue. This
        operation removes the item from the queue.
        """
        return self.list.pop()

    def isEmpty(self):
        "Returns true if the queue is empty"
        return len(self.list) == 0

class ShopBot:

    def __init__(self):
        self.greetings = ["hey", "hello", "hi", "howdy", "great to see you", "thanks for coming in today"]
        self.openings = ["what'll it be?", "what can i do ya for?", "what can i get started for you?", "do you know what you'd like?"]
        self.confirmations = ["sure thing", "no problem", "coming right up", "you got it", "of course"]
        self.checking = ["What else"]
        self.positives = ["bingo", "yay", "yes", "yeah", "absolutely", "correct", "yup", "perfect", "great", "sure"]
        self.negatives = ["no", "nope", "incorrect", "wrong"]
        self.lastInstructions = []
        self.ngrams = []
        self.exceptionQueue = None

    def listenToCustomer(self):
        userInput = input()
        cleanUserInput = ShopBot.cleanInput(userInput)
        self.lastInstructions.append(cleanUserInput)
        userTokens = cleanUserInput.split() 
        tupleContainer = []
        for i in range(1,5):
            ngramTuple = self.getNgrams(userTokens, i)
            # print(ngramTuple)
            ngramList = [ngram for ngram in ngramTuple]
            # print(ngramList)
            tupleContainer.append(ngramList)
            # print(tupleContainer)
        flatTuples = [item for sublist in tupleContainer for item in sublist]
        self.ngrams.append(flatTuples)

    def confirmResponse(self, response):
        cleanResponse = ShopBot.cleanInput(response)
        for pos in self.positives:
            if cleanResponse.find(pos) != -1:
                return True
        return False

    # Function that takes token list of strings and creates custom length n-grams
    # Instead of dynamically setting n-grams n, could return everything below a number based on string length
    def getNgrams(self, tokens, n=3):
        nowNgrams = []
        for idx in range(len(tokens)-n+1):
            yield tuple(tokens[idx:idx+n])

    def menuDialogue(self, menub):
        # print(random.choice(self.confirmations))
        menub.readMenu()
        menub.menuRead = True
        print('Server: ', random.choice(self.openings))

    def orderDialogue(self):
        orderSammy = None
        orderExcept = []

        for ngram in self.ngrams[-1]:
            # print(ngram)
            ngramString = " ".join(ngram)
            # print(ngramString)
            for word in langref.modificationList:
                if ngramString.startswith(word) and len(ngram) > 1:
                    orderExcept.append(ngram)

            for sammy in menu.sandwichDf["name"].unique():
                if orderSammy is not None:
                    break
                if (self.editDist(ngramString, sammy, len(ngramString), len(sammy)) <= .3): # removed "or" conditional (ngramString.find(sammy) > -1) because "club" was matching multiple sammies
                    print('Server: ', f"You would like the {sammy}, correct?")
                    sammyConfirmation = input()
                    if self.confirmResponse(sammyConfirmation):
                        orderSammy = sammy
                        break
                    else:
                        continue

        if orderSammy is None:
            print("Server: I'm terribly sorry I don't think we make that sandwich here.  Is there something else I can get you?")
        else:
            orderExcept = list(set(orderExcept))
        return orderSammy, orderExcept

    # Function to take user input(), remove special characters, stop words, make all lower case, and map equivelants
    @staticmethod
    def cleanInput(inputString):
        alphanumInput = re.sub(r"[^A-Za-z0-9 ]+", "", inputString)
        lowerSingularNoStops = [langref.makeSingular(word.lower()) for word in alphanumInput.split() if word.lower() not in langref.stopWords]
        mappedEquivelants = []
        for word in lowerSingularNoStops:
            mappedWord = langref.equivelantTerms.get(word)
            if mappedWord:
                mappedEquivelants.append(mappedWord)
            else:
                mappedEquivelants.append(word)
        outputString = " ".join(mappedEquivelants)
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