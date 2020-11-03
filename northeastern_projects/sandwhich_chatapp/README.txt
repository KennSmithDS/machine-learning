Step 1

Menu Offerings:

1) kendalls sour club comes with spam camembert cheese onion saeurkraut pickle and siracha dressed with mustard thousand island ranch and vinegar on sourdough
2) classic turkey club comes with turkey and bacon pepper jack cheese tomato and lettuce dressed with mayo on white
3) italian club comes with ham and salami provolone cheese onion lettuce tomato and peperoncino dressed with mayo olive oil and vinegar on white
4) beach club comes with tuna provolone cheese lettuce tomato cucumber and avocado dressed with mayo on white
5) veggie club comes with hummus onion lettuce tomato cucumber avocado and bell pepper dressed with vinegar on wheat
6) grilled cheese comes with american cheese dressed with mayo on white
7) classic reuben comes with beef swiss cheese saeurkraut dressed with thousand island on rye
8) grilled pbjb comes with bacon dressed with peanut butter and jelly on white

Exception Offerings:

Bread:

 - lettuce
 - white
 - wheat
 - rye
 - sourdough
 - french

Dressing:

 - olive oil
 - vinegar
 - ranch
 - mayo
 - mustard
 - thousand island
 - salt
 - pepper
 - peanut butter
 - jelly
 - sriracha

Cheese:

 - provolone
 - camembert
 - swiss
 - american
 - cheddar
 - pepper jack

Meat:

 - bacon
 - spam
 - beef
 - turkey
 - tuna
 - ham
 - salami
 - chicken

Veggie:

 - saeurkraut
 - lettuce
 - tomato
 - cucumber
 - avocado
 - onion
 - olive
 - bell pepper
 - peperoncino
 - pickle
 
Step 2
 
Equivalent Terms (see langref.py for reference):

Veggie <- 'veg': 'veggie', 'vegetable': 'veggie', 'vegetarian': 'veggie', 
Meat <- 'flesh': 'meat', 'fleshy': 'meat', 'animal': 'meat', 'bird': 'meat', 'turkey': 'meat', 'beef': 'meat', 'egg': 'meat', 'cow': 'meat', 'pig': 'meat', 'pork': 'meat',
Cheese <- 'cheesy': 'cheese', 'queso': 'cheese', 'cheeses': 'cheese', 'curd': 'cheese',
Bread <- 'breadstuff': 'bread', 'dough': 'bread', 'wrapping': 'bread', 'pain': 'bread', 'loaf': 'bread', 'toast': 'bread', 'roll': 'bread'
Dressing <- 'sauce': 'dressing', 'relish': 'dressing', 'topping': 'dressing', 'condiment': 'dressing', 'seasoning': 'dressing', 'mayo': 'mayo', 'mayonnaise': 'mayo', 'pbj': 'peanut butter jelly', 'spread': 'dressing'
 
Ignored Terms a.k.a Stop Words (see langref.py for reference):
 
["i","would","like","please","thank","you","order","give","me","want","let","have","this",
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
"wouldnt","youd","youll","youre","youve","your","yours","yourself","yourselves","yet"]

Exception Flag Terms (see langref.py for reference):

exceptionWords = ["hold", "no", "without", "remove"]
additionWords = ["extra", "with", "add", "more"]
substitutionWords = ["sub", "substitute", "swap", "exchange"]

Step 3

Required Environment:

Python 3+ with a few additional packages you will need to install if not already in your environment:
 - pandas: to store the menu items as a dataframe object (simple database like lookup)
 - pillow: to display sandwich image at the end when order is confirmed
 
Running Instructions:

1) Open command line environment or IDE

If in command line:

2) Change directory <cd> to the folder "kendall_smith_assign4"
3) Type the command "python shop.py" to launch the application
4) Follow the prompts from the application:
	- You can do things like ask for menu or ingredient options
	- You can also request your sandwich from the menu, and make exeptions
	
If in IDE (e.g. VS Code):

2) Choose "Menu -> Open Folder"
3) Navigate to the folder "kendall_smith_assign4"
4) Right click on shop.py to "Run Python File in Terminal"
5) Follow the prompts from the application:
	- You can do things like ask for menu or ingredient options
	- You can also request your sandwich from the menu, and make exeptions
	
Included Files for Implementation:

 - shop.py : primary application file that drives the state machine and makes successive calls to class methods
 - chatbot.py : contains class object with attributes and methods for how the shop chatbot interacts with the customer, e.g. performs text preprocessing and tokenization, creates ngrams, drives different kinds of dialogue
 - menu.py : contins class object with attributes and methods for containing and reading off the menu options
 - order.py : contains class object with attributes and methods for adding sandwiches to customer order, printing and confirming order contents
 - sandwich.py : contains class object with attributes and methods for making the sandwich, and performing exceptions, additions and substitutions, as well as displaying sandwich image (maybe could be menu method?)
 - langref.py : contains reference resources for language look up, e.g. english stop words, equivelancy mapping, and making plurals to singular
	
Step 4

Example 1

####################################################################################################
################################ WELCOME TO KENDALLS SANDWICH SHOP  ################################
####################################################################################################

Server:  great to see you, do you know what you'd like?
What are your specials today?
Server:  of course
----------------------------------------------------------------------------------------------------
Server:  These are our 8 specials today:
1) kendalls sour club comes with spam camembert cheese onion saeurkraut pickle and sriracha dressed with mustard thousand island ranch and vinegar on sourdough
2) classic turkey club comes with turkey and bacon pepper jack cheese tomato and lettuce dressed with mayo on white
3) italian club comes with ham and salami provolone cheese onion lettuce tomato and peperoncino dressed with mayo olive oil and vinegar on white
4) beach club comes with tuna provolone cheese lettuce tomato cucumber and avocado dressed with mayo on white
5) veggie club comes with hummus onion lettuce tomato cucumber avocado and bell pepper dressed with vinegar on wheat
6) grilled cheese comes with american cheese dressed with mayo on white
7) classic reuben comes with beef swiss cheese saeurkraut dressed with thousand island on rye
8) grilled peanut butter jelly bacon comes with bacon dressed with peanut butter and jelly on white
----------------------------------------------------------------------------------------------------
Server:  what'll it be?
Make me a classic reuben with extra swiss
Server:  you got it
Server:  You would like the classic reuben, correct?
yes
What kind of bread would you like?  The classic reuben usually comes with rye
wheat
What kind of spread/dressing would you like? classic reuben usually comes with thousand island
Just put what usually comes on that
Server: I would like to confirm your order...
Server: So, you have ordered 1 item(s) so far.  Here is what I have written down:
Server: Your classic reuben comes with beef swiss cheese saeurkraut dressed with thousand island on wheat
Server: Does that sound about right?
Yes, thanks!
Server: Give me a minute while I make that for you!
Server: Here's your sandwich!

####################################################################################################
########################## THANKS FOR SHOPPING AT KENDALLS SANDWICH SHOP  ##########################
####################################################################################################

Example 2

####################################################################################################
################################ WELCOME TO KENDALLS SANDWICH SHOP  ################################
####################################################################################################

Server:  howdy, what can i do ya for?
Hi I'll take a beach club but add onions please
Server:  of course
Server:  You would like the beach club, correct?
yes
What kind of bread would you like?  The beach club usually comes with white
what other bread options do you have?
Server:  Your bread options are:
 -  lettuce
 -  white
 -  wheat
 -  rye
 -  french bread
 -  sourdough
how about sourdough
What kind of spread/dressing would you like? beach club usually comes with mayo
that should be good
Server: I would like to confirm your order...
Server: So, you have ordered 1 item(s) so far.  Here is what I have written down:
Server: Your beach club comes with tuna provolone cheese lettuce tomato cucumber avocado and onion dressed with mayo on sourdough
Server: Does that sound about right?
correct
Server: Give me a minute while I make that for you!
Server: Here's your sandwich!

####################################################################################################
########################## THANKS FOR SHOPPING AT KENDALLS SANDWICH SHOP  ##########################
####################################################################################################

Example 3

####################################################################################################
################################ WELCOME TO KENDALLS SANDWICH SHOP  ################################
####################################################################################################

Server:  thanks for coming in today, what can i get started for you?
hello what's on the menu?
Server:  of course
----------------------------------------------------------------------------------------------------
Server:  These are our 8 specials today:
1) kendalls sour club comes with spam camembert cheese onion saeurkraut pickle and sriracha dressed with mustard thousand island ranch and vinegar on sourdough
2) classic turkey club comes with turkey and bacon pepper jack cheese tomato and lettuce dressed with mayo on white
3) italian club comes with ham and salami provolone cheese onion lettuce tomato and peperoncino dressed with mayo olive oil and vinegar on white
4) beach club comes with tuna provolone cheese lettuce tomato cucumber and avocado dressed with mayo on white
5) veggie club comes with hummus onion lettuce tomato cucumber avocado and bell pepper dressed with vinegar on wheat
6) grilled cheese comes with american cheese dressed with mayo on white
7) classic reuben comes with beef swiss cheese saeurkraut dressed with thousand island on rye
8) grilled peanut butter jelly bacon comes with bacon dressed with peanut butter and jelly on white
----------------------------------------------------------------------------------------------------
Server:  what can i get started for you?
oh man, can i get a grilled peanut butter jelly and bacon please?  that sounds so good!
Server:  no problem
Server:  You would like the grilled peanut butter jelly bacon, correct?
yup
What kind of bread would you like?  The grilled peanut butter jelly bacon usually comes with white
whatever you usually put it on is fine
What kind of spread/dressing would you like? grilled peanut butter jelly bacon usually comes with peanut butter and jelly
i would like some sriracha as well please
Server: I would like to confirm your order...
Server: So, you have ordered 1 item(s) so far.  Here is what I have written down:
Server: Your grilled peanut butter jelly bacon comes with bacon dressed with sriracha on white
Server: Does that sound about right?
sounds perfect
Server: Give me a minute while I make that for you!
Server: Here's your sandwich!

####################################################################################################
########################## THANKS FOR SHOPPING AT KENDALLS SANDWICH SHOP  ##########################
####################################################################################################

Example 4 - (failure)

####################################################################################################
################################ WELCOME TO KENDALLS SANDWICH SHOP  ################################
####################################################################################################

Server:  howdy, what can i do ya for?
yo, can you make me a french dip?
Server:  coming right up
Server: I'm terribly sorry I don't think we make that sandwich here.  Is there something else I can get you?
what other choice are there?
----------------------------------------------------------------------------------------------------
Server:  These are our 8 specials today:
1) kendalls sour club comes with spam camembert cheese onion saeurkraut pickle and sriracha dressed with mustard 
thousand island ranch and vinegar on sourdough
2) classic turkey club comes with turkey and bacon pepper jack cheese tomato and lettuce dressed with mayo on white
3) italian club comes with ham and salami provolone cheese onion lettuce tomato and peperoncino dressed with mayo olive oil and vinegar on white
4) beach club comes with tuna provolone cheese lettuce tomato cucumber and avocado dressed with mayo on white    
5) veggie club comes with hummus onion lettuce tomato cucumber avocado and bell pepper dressed with vinegar on wheat
6) grilled cheese comes with american cheese dressed with mayo on white
7) classic reuben comes with beef swiss cheese saeurkraut dressed with thousand island on rye
8) grilled peanut butter jelly bacon comes with bacon dressed with peanut butter and jelly on white
----------------------------------------------------------------------------------------------------
Server:  what can i get started for you?
maybe I'll try kendalls sour club
Server:  of course
Server:  You would like the kendalls sour club, correct?
yup
What kind of bread would you like?  The kendalls sour club usually comes with sourdough
i want millenial artisan bread
Server: I'm sorry but we don't have millenial
Server: I'm sorry but we don't have artisan
Server: I'm sorry but we don't have bread
What kind of spread/dressing would you like? kendalls sour club usually comes with mustard thousand island ranch 
and vinegar
what other choice for spreads do you have?
Server:  Your dressing options are:
 -  olive oil
 -  vinegar
 -  ranch
 -  mayo
 -  mustard
 -  thousand island
 -  salt
 -  pepper
 -  peanut butter
 -  jelly
 -  sriracha
give me all of those
Server: I would like to confirm your order...
Server: So, you have ordered 1 item(s) so far.  Here is what I have written down:
Server: Your kendalls sour club comes with spam camembert cheese onion saeurkraut pickle and sriracha dressed with on
Server: Does that sound about right?
No you didn't give me the bread I wanted, nor did you add the dressings i asked for
Server: I'm sorry about that, could you please repeat your order?
No, this is such terrible customer service, I'm hiring CatterBot!
Server: I'm terribly sorry I don't think we make that sandwich here.  Is there something else I can get you?     
For peeps sake, NO!
Server: I'm sorry we couldn't be of more assistance to you today, take care

####################################################################################################
########################## THANKS FOR SHOPPING AT KENDALLS SANDWICH SHOP  ##########################
####################################################################################################

Reflection on Failed Scenario:

The system fails in this example for a few different reasons.  First, it doesnt' have a good way of handling logically when a customer asks for something not on the menu.  The state machine is able to loop back to identifying a sandwhich but not making consecutive customizations.  Second, in the applications current state, it is unable to add all ingredients of a particular type to the sandwich.  If the customer never entered a valid sandwich name, the program would default to exit.

Step 5

Easiest Part of Assignment

The easiest part of the assignment was deciding what ingredients to have on each sandwich as this only took a few minutes of time researching on the internet.  The process for creating classes for the order, sandwich, and menu were fairly easy to design and implement.

Hardest Part of Assignment

The hardest part of this assignment was multifold, 1) building out thorough logic to handle all the different kinds of ways requests can be made in the English language, and 2) designing the state-machine like logic to keep the conversation going and loop through the main "stages" of taking and order to completion.

Learnings/Takeaways from Assignment

I learned the value in doing things the hard way first, becuase it forces one to start with subproblems and implement components that should be able to integrate into the bigger picture.  This of course requires spending time thinking out the logical architecture of the program in advance, and really helped to define the scope of the different class objects, their respective methods/attributes, and how each piece fit into the larger workflow.