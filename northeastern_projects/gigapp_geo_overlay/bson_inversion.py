#MAIN CODE: https://www.kaggle.com/inversion/processing-bson-files
#Help Multiprocessing: https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue
#Help JSONEncoder: https://stackoverflow.com/questions/16586180/typeerror-objectid-is-not-json-serializable

#------ Import
import bson #Install via: conda/pip install pymongo
import multiprocessing as mp #Dispatch the workload
import json #To dump the data into a file with JSON format
import sys #For the progress bar
import datetime #Handles ISODate entries
import pickle

#------ Settings
NCORE = 4 #Number of worker you want the dispatch the process into
DETAILS = 20000 #Update on the % every DETAILS requests
TOTAL = 7076585 #Number of transactions in the file 

matchResults = mp.Manager().dict() # note the difference
trackedUsernames = ['astrobel', 'Karla-CornejoPotter', 'Martin-Martinez-41', 'Denise-Hankins-McLin',\
					'Shalia-Davila', 'Emily-Lavery-1', 'John-Wick'] 
					#The usernames you want to search for (these were selected randomly...)


#------ Define the worker function and the necessary variables

def processFunc(q, iolock):
	while True:
		d = q.get()
		if d is None:
			break
		#print(d)

		username = None
		try:
			targetIn = d['payment']['target']['user']['username'] in trackedUsernames
			actorIn = d['payment']['actor']['username'] in trackedUsernames
		except:
			targetIn = False
			actorIn = False
		#print(targetIn, actorIn)

		if targetIn:
			username = d['payment']['target']['user']['username']
		elif actorIn:
			username = d['payment']['actor']['username']
		else:
			continue
		
		#Add the username to matchResults
		if username not in matchResults:
			matchResults[username] = [d]
		else:
			matchResults[username].append(d)


q = mp.Queue(maxsize=NCORE)
iolock = mp.Lock()
pool = mp.Pool(NCORE, initializer=processFunc, initargs=(q, iolock))

#------ Process the file
print('---------- Starting search...\n')

data = bson.decode_file_iter(open('./venmo.bson', 'rb'))
for c, d in enumerate(data):
	if c % DETAILS == 0:
		    sys.stdout.write("\r{} % - {} Transactions".format(round(c*100/TOTAL, 2), c))

	q.put(d)  # blocks until q below its max size


#Tell workers we're done
for _ in range(NCORE): #To break the while True in the processFunc
	q.put(None)

pool.close()
pool.join()

#------ Convert back to normal dictionary and dump in a JSON file.
matchResults = dict(matchResults)

pickle.dump(matchResults, open("results.p", "wb")) #Save into a pickle file

class JSONEncoder(json.JSONEncoder): #Redefine the way we encode bson.ObjectId objects
	def default(self, o):
		if isinstance(o, bson.ObjectId):
			return str(o)
		elif isinstance(o, (datetime.date, datetime.datetime)):
			return o.isoformat()
		return json.JSONEncoder.default(self, o)

matchResults = JSONEncoder().encode(matchResults)

with open('results.json', 'w') as fp:
    fp.write(matchResults) #Save into a .JSON file

print('\n--------\n', matchResults)