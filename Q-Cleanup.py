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
		minimum = 200
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
		#if (os.path.isfile('Q-Table.txt') == True):
		#	with open("Q-table.txt", "r") as QTablefile:
		#		Q = json.load(QTablefile)
		#		print(f"Q-table uploaded with {len(Q)} lines")	
		textInput = input("Enter the iteration to be updated in Q with brackets: ")
		textInput = textInput[1:-1]
		itemList = [int(item) for item in textInput.split(',')]
		print(itemList)
		updateList = itemList.copy()[:88]
		while(len(updateList) > 3):
			itemFound = False
			for item in Q:
				if interimList == item[0]:
					item[2] = 1
					itemFound = True
					break
			if (itemFound == False):
				print(f"{updateList} has not been found")
			updateList.pop()
		#with open("Q-table.txt","w") as handler:
		#	json.dump(Q,handler) 
		#handler.close()    

#QCleanup.cleanser()	
QCleanup.reader(4)
#QCleanup.updateFrom88()
