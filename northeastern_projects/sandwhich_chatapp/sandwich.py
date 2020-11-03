""" 
contains class object with attributes and methods for making the sandwich, and performing exceptions, additions and substitutions, as well as displaying sandwich image
"""

from PIL import Image
import os

class Sandwich:
    def __init__(self, name, bread, dressing, meat, cheese, veggie):
        self.name = name
        self.bread = bread
        self.dressing = dressing
        self.meat = meat
        self.cheese = cheese
        self.veggie = veggie

    def makeException(self, itemType, itemToRemove):
        # print(f"Server: no {itemToRemove}")
        if itemType == 'bread':
            if itemToRemove in self.bread:
                self.bread.remove(itemToRemove)
        elif itemType == 'dressing':
            if itemToRemove in self.dressing:
                self.dressing.remove(itemToRemove)
        elif itemType == 'meat':
            if itemToRemove in self.meat:
                self.meat.remove(itemToRemove)
        elif itemType == 'cheese':
            if itemToRemove in self.cheese:
                self.cheese.remove(itemToRemove)
        elif itemType == 'veggie':
            if itemToRemove in self.veggie:
                self.veggie.remove(itemToRemove)

    def makeAddition(self, itemType, itemToAdd):
        # print(f"Server: with {itemToAdd}")
        if itemType == 'bread':
            self.bread.append(itemToAdd)
        elif itemType == 'dressing':
            self.dressing.append(itemToAdd)
        elif itemType == 'meat':
            self.meat.append(itemToAdd)
        elif itemType == 'cheese':
            self.cheese.append(itemToAdd)
        elif itemType == 'veggie':
            self.veggie.append(itemToAdd)

    def showSandwich(self):
        sammyJpg = self.jpgLookup()
        jpgPath = os.path.join("images", sammyJpg)
        sammyImg = Image.open(jpgPath)
        sammyImg.show()

    def jpgLookup(self):
        imageLookupDict = {
            "kendalls sour club": "kendall.jpg",
            "classic turkey club": "turkey.jpg",
            "italian club": "italian.jpg",
            "beach club": "beach.jpg",
            "veggie club": "veggie.jpg",
            "grilled cheese": "cheese.jpg",
            "classic reuben": "reuben.jpg",
            "grilled peanut butter jelly bacon": "pbjb.jpg"
            }
        return imageLookupDict[self.name]