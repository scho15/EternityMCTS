import json
import os.path
from collections import Counter

class QCleanup:
	# Simple file to read Q and see if any entries exceed 88 (and Q can be "dumped" back in edited form)
	# Could use later to sort through Q and see some interesting properties
	def cleanser():
		Q = []
		a = []		
		if (os.path.isfile('Q-Table.txt') == True):
			with open("Q-table.txt", "r") as QTablefile:
				Q = json.load(QTablefile)
				print(f"Q-table uploaded with {len(Q)} lines")
		for item in Q:
			length = len(item[0])
			a.append(length)
		print(f"Maximum and average are {max(a)} and {sum(a)/len(a):.5f}\n")
		print(sorted(Counter(a).items()))
		a.clear()
		for item in Q.copy():
			if (len(item[0]) > 88):
				Q.remove(item)
		for item in Q:
			length = len(item[0])
			a.append(length)
		print(f"Revised maximum and average are {max(a)} and {sum(a)/len(a):.5f} and length is {len(Q)}\n")
		print(sorted(Counter(a).items()))
		#with open("Q-table.txt","w") as handler:
		#	json.dump(Q,handler) 
		#handler.close()    

	def massedit(iteration):
		Q = []
		counter = 0
		if (os.path.isfile('Q-Table.txt') == True):
			with open("Q-table.txt", "r") as QTablefile:
				Q = json.load(QTablefile)
				print(f"Q-table uploaded with {len(Q)} lines")
		for item in Q.copy():
			if (len(item[0]) == iteration and item[2] > 0):
				item[2] = 0
				counter = counter + 1
		print(f"Number of items amended to length 0 for iteration {iteration} was {counter}")
		with open("Q-table.txt","w") as handler:
			json.dump(Q,handler) 
		handler.close()    

	def reader(iteration):
		Q = []
		sum = 0
		minimum = 205
		QDictLength = {}
		QDictVisits = {}
		if (os.path.isfile('Q-Table.txt') == True):
			with open("Q-table.txt", "r") as QTablefile:
				Q = json.load(QTablefile)
				print(f"Q-table uploaded with {len(Q)} lines")
		for item in Q:
			length = len(item[0])
			if (length == iteration and item[1] >= minimum):
				QDictLength[str(item[0])] = item[1] # 1 for iteration and 2 for visit
				QDictVisits[str(item[0])] = item[2]
				sum += 1
		print(f"Entries which are {minimum} or more are {sum}")
		#print(sorted(QDictLength.items(), key=lambda x: x[1], reverse=True))
		#print(sorted(QDictVisits.items(), key=lambda x: x[1], reverse=True))
		entries = sorted(QDictLength.items(), key=lambda x: x[1], reverse=True)
		for element in entries:			
			print(f"{element[0]}, {element[1]}, {QDictVisits[element[0]]}")

	def updateFrom88():
		Q = []
		itemList = []
		updateList = []
		textInput = ""
		errorNote = False
		if (os.path.isfile('Q-Table.txt') == True):
			with open("Q-table.txt", "r") as QTablefile:
				Q = json.load(QTablefile)
				print(f"Q-table uploaded with {len(Q)} lines")	
		textInput = input("Enter the iteration to be updated in Q with brackets: ")
		textInput = textInput[1:-1]
		itemList = [int(item) for item in textInput.split(',')]
		updateList = itemList.copy()[:88]
		while(len(updateList) > 3):
			itemFound = False
			for item in Q:
				if updateList == item[0]:
					item[2] = 1
					itemFound = True
					break
			if (itemFound == False):
				print(f"{updateList} has not been found")
				errorNote = True
			updateList.pop()
		if (errorNote == True):
			print("There was a problem on at least one update")
		else:
			print("All entries were updated successfully")
		with open("Q-table.txt","w") as handler:
			json.dump(Q,handler) 
		handler.close()  
		
	def iterationReader():
		values = []
		values
		textInput = input("Enter the list of viable iterations: ")
		textInput = textInput[1:-1]
		itemList = [int(item) for item in textInput.split(',')]
		print(f"itemList is {sorted(Counter(itemList).items())}")
		#itemList is [(188, 1), (191, 2), (194, 4), (195, 15), (196, 24), (197, 69), (198, 60), (199, 47), (200, 43), (201, 21), (202, 12), (203, 4), (204, 2), (207, 1)]
		#itemList is [(193, 1), (194, 8), (195, 9), (196, 33), (197, 43), (198, 50), (199, 43), (200, 33), (201, 31), (202, 8), (203, 6), (204, 3), (207, 1)]
		#itemList is [(190, 1), (191, 5), (194, 5), (195, 13), (196, 28), (197, 54), (198, 57), (199, 45), (200, 26), (201, 27), (202, 12), (203, 5), (204, 1)]
		#itemList is [(187, 1), (191, 4), (193, 3), (194, 6), (195, 14), (196, 41), (197, 52), (198, 78), (199, 50), (200, 24), (201, 19), (202, 5), (203, 3), (204, 3), (206, 2), (207, 1)]
		#itemList is [(191, 1), (193, 1), (194, 2), (195, 11), (196, 18), (197, 42), (198, 63), (199, 48), (200, 44), (201, 26), (202, 10), (203, 4), (204, 6), (205, 3)]
#QCleanup.cleanser()	
#QCleanup.reader(2)
QCleanup.iterationReader()
