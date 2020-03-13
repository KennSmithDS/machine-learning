import pandas as pd
import os

# Test preprocessing functions to handle user input
stopWords = ["i","would","like","please","thank","you","order","give","me","want","let","have","this",
    "on","it","the","but","a","about","above","after","again","against","all","am","an","any","are","arent",
    "as","at","be","because","been","before","being","below","between","both","by","cant","cannot","could",
    "couldnt","did","didnt","do","does","doesnt","doing","down","during","each","few","for","from",
    "further","had","hadnt","has","hasnt","havent","having","he","hed","hell","hes","her","here","heres",
    "hers","herself","him","himself","his","how","hows","id","ill","im","ive","if","in","into","is","isnt",
    "its","its","itself","lets","more","most","mustnt","my","myself","of","off","once",
    "only","other","ought","our","ours","ourselves","out","over","own","same","shant","she","shed","shell",
    "shes","should","shouldnt","so","some","such","than","that","thats","their","theirs","them","themselves",
    "then","there","theres","these","they","theyd","theyll","theyre","theyve","this","those","through","to",
    "too","under","until","up","very","was","wasnt","we","wed","well","were","weve","were","werent","when",
    "whens","where","wheres","which","while","who","whos","whom","why","whys","with","wont","what","whats"
    "wouldnt","youd","youll","youre","youve","your","yours","yourself","yourselves"]

whichDictList = [
    {'name': 'kendalls sour special', 'bread': ['sourdough'], 'dressing': ['mustard','thousand island','ranch','vinegar'], 'cheese': ['camembert'], 'meat': ['spam'], 'veggie': ['onion','saeurkraut','pickle']},
    {'name': 'classic turkey club', 'bread': ['white'], 'dressing': ['mayo'], 'cheese': ['pepper jack'], 'meat': ['turkey','bacon'], 'veggie': ['tomato','lettuce']},
    {'name': 'italian club', 'bread': ['white'], 'dressing': ['mayo','olive oil','vinegar'], 'cheese': ['provolone'], 'meat': ['ham','salami'], 'veggie': ['onion','lettuce','tomato','peperoncino']},
    {'name': 'beach club', 'bread': ['white'], 'dressing': ['mayo'], 'cheese': ['provolone'], 'meat': ['tuna'], 'veggie': ['lettuce','tomato','cucumber','avocado']},
    {'name': 'veggie club', 'bread': ['wheat'], 'dressing': ['vinegar'], 'cheese': [], 'meat': [], 'veggie': ['hummus','onion','lettuce','tomato','cucumber','avocado','bell pepper']},
    {'name': 'grilled cheese', 'bread': ['white'], 'dressing': ['mayo'], 'cheese': ['american'], 'meat': [], 'veggie': []},
    {'name': 'classic reuben', 'bread': ['rye'], 'dressing': ['thousand island'], 'cheese': ['swiss'], 'meat': ['beef'], 'veggie': ['saeurkraut']},
    {'name': 'grilled pbjb', 'bread':['white'], 'dressing': ['peanut butter','jelly'], 'cheese': [], 'meat':['bacon'], 'veggie':[]}]
sandwhichDf = pd.DataFrame(whichDictList)
# print(sandwhichDf.head())

ingredDictList = [
    {'ingredient': 'lettuce', 'type': 'bread'},{'ingredient': 'white', 'type': 'bread'},{'ingredient': 'wheat', 'type': 'bread'},
    {'ingredient': 'rye', 'type': 'bread'},{'ingredient': 'olive oil', 'type': 'dressing'},{'ingredient': 'vinegar', 'type': 'dressing'},
    {'ingredient': 'ranch', 'type': 'dressing'},{'ingredient': 'mayo', 'type': 'dressing'},{'ingredient': 'mustard', 'type': 'dressing'},
    {'ingredient': 'thousand island', 'type': 'dressing'},{'ingredient': 'salt', 'type': 'dressing'},{'ingredient': 'pepper', 'type': 'dressing'},
    {'ingredient': 'peanut butter', 'type': 'dressing'},{'ingredient': 'jelly', 'type': 'dressing'},{'ingredient': 'bacon', 'type': 'meat'},
    {'ingredient': 'spam', 'type': 'meat'},{'ingredient': 'beef', 'type': 'meat'},{'ingredient': 'turky', 'type': 'meat'},
    {'ingredient': 'tuna', 'type': 'meat'},{'ingredient': 'ham', 'type': 'meat'},{'ingredient': 'salami', 'type': 'meat'},
    {'ingredient': 'chicken', 'type': 'meat'},{'ingredient': 'provolone', 'type': 'cheese'},{'ingredient': 'camembert', 'type': 'cheese'},
    {'ingredient': 'swiss', 'type': 'cheese'},{'ingredient': 'american', 'type': 'cheese'},{'ingredient': 'cheddar', 'type': 'cheese'},
    {'ingredient': 'pepper jack', 'type': 'cheese'},{'ingredient': 'saeurkraut', 'type': 'veggie'},{'ingredient': 'lettuce', 'type': 'veggie'},
    {'ingredient': 'tomato', 'type': 'veggie'},{'ingredient': 'cucumber', 'type': 'veggie'},{'ingredient': 'avocado', 'type': 'veggie'},
    {'ingredient': 'onion', 'type': 'veggie'},{'ingredient': 'olive', 'type': 'veggie'},{'ingredient': 'bell pepper', 'type': 'veggie'},
    {'ingredient': 'peperoncino', 'type': 'veggie'},{'ingredient': 'pickle', 'type': 'veggie'}, {'ingredient': 'sourdough', 'type': 'bread'}]
ingredientDf = pd.DataFrame(ingredDictList)
# print(ingredientDf.head())