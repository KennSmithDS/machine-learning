"""
contains reference resources for language look up, e.g. english stop words, equivelancy mapping, and making plurals to singular
"""

# Text preprocessing objects to handle user input
stopWords = ["i","would","like","please","thank","you","order","give","me","want","let","have","this",
    "on","it","the","but","a","about","above","after","again","against","all","am","an","any","are","arent",
    "as","at","be","because","been","before","being","below","between","both","by","cant","cannot","could",
    "couldnt","did","didnt","do","does","doesnt","doing","down","during","each","few","for","from",
    "further","had","hadnt","has","hasnt","havent","having","he","hed","hell","hes","her","here","heres",
    "hers","herself","him","himself","his","how","hows","id","ill","im","ive","if","in","into","is","isnt",
    "its","its","itself","lets","more","most","mustnt","my","myself","of","off","once","thanks",
    "only","other","ought","our","ours","ourselves","out","over","own","same","shant","she","shed","shell",
    "shes","should","shouldnt","so","some","such","than","that","thats","their","theirs","them","themselves",
    "then","there","theres","these","they","theyd","theyll","theyre","theyve","this","those","through","to",
    "too","under","until","up","very","was","wasnt","we","wed","well","were","weve","were","werent","when",
    "whens","where","wheres","which","while","who","whos","whom","why","whys","wont","what","whats"
    "wouldnt","youd","youll","youre","youve","your","yours","yourself","yourselves","yet","can","put"]

modificationList = ["hold", "no", "without", "remove", "extra", "with", "add", "more", "sub", "substitute", "swap", "exchange"]
exceptionWords = ["hold", "no", "without", "remove"]
additionWords = ["extra", "with", "add", "more"]
substitutionWords = ["sub", "substitute", "swap", "exchange"]

equivelantTerms = {
    'veggie': 'veggie', 'nonmeat': 'veggie', 'veg': 'veggie', 'vegetable': 'veggie', 'vegetarian': 'veggie', 
    'meat': 'meat', 'flesh': 'meat', 'fleshy': 'meat', 'animal': 'meat', 'bird': 'meat', 'beef': 'meat', 'egg': 'meat', 'cow': 'meat', 'pig': 'meat', 'pork': 'meat', 'chicken': 'meat',
    'cheese': 'cheese', 'cheesy': 'cheese', 'queso': 'cheese', 'cheeses': 'cheese', 'curd': 'cheese',
    'bread': 'bread', 'breadstuff': 'bread', 'dough': 'bread', 'wrapping': 'bread', 'pain': 'bread', 'loaf': 'bread', 'toast': 'bread', 'roll': 'bread',
    'dressing': 'dressing', 'sauce': 'dressing', 'relish': 'dressing', 'topping': 'dressing', 'condiment': 'dressing', 'seasoning': 'dressing', 'mayo': 'mayo', 'mayonnaise': 'mayo', 'pbj': 'peanut butter jelly', 'spread': 'dressing'
}

letters = list(map(chr, range(97, 123))) 
vowels = ["a", "e", "i", "o", "u"]
consonants = [letter for letter in letters if letter not in vowels]
specialNounEndings = ["ch", "sh", "ss", "s", "x", "z"]
posneg = ["no", "nope", "incorrect", "wrong","bingo", "yay", "yes", "yeah", "absolutely", "correct", "yup"]

def makeSingular(word):
    if word not in posneg:
        if word == "veggies":
            return "veggie"
        if word[-3:] == "ies":
            return word[:-3] + "y"
        if word[-3:] == "ves":
            return word[:-3] + "f"
        if word[-2:] == "es" and (word[-4:-2] in specialNounEndings or word[-3] in specialNounEndings):
            return word[:-2]
        if word[-2:] == "es" and word[-4] in consonants and word[-3] in vowels:
            return word[:-2]
        if word[-2:] == "es":
            return word[:-1]
        if word[-1] == "s":
            return word[:-1]
    return word