import json
import os.path
from collections import Counter

class QCleanup:
	# Simple file to read Q and see if any entries exceed 88 (and Q can be "dumped" back in edited form)
	# Could use later to sort through Q and see some interesting properties
	def cleanser():
		Q = []
		a = []	
		b = []
		cutoff = 190
		minimumIteration = 6
		counter = 0
		kept = 0
		if (os.path.isfile('C:/Users/scho1/QTableMCTS/QTable.txt') == True):
			with open("C:/Users/scho1/QTableMCTS/QTable.txt", "r") as QTablefile:
				Q = json.load(QTablefile)
				print(f"QTable uploaded with {len(Q)} lines")
		for item in Q:
			length = len(item[0])
			a.append(length)
			b.append(item[1])
		print(f"Maximum and average iterations are {max(a)} and {sum(a)/len(a):.5f}")
		print(sorted(Counter(a).items()))
		a.clear()
		print(f"Maximum and average lengths are {max(b)} and {sum(b)/len(b):.5f}")
		print(sorted(Counter(b).items()))
		b.clear()
		print(f"\nIntroducing a minimum cutoff of {cutoff} for iterations for those greater than length {minimumIteration}")
		for item in Q.copy():
			if (item[1] < cutoff and len(item[0]) > minimumIteration):
				Q.remove(item)				
				counter += 1
				if (counter%10000 == 0):
					print(f"{counter} items have been removed and items kept is {kept}")
			else:
				kept += 1
		for item in Q:
			length = len(item[0])
			a.append(length)
			b.append(item[1])
		print(f"Revised maximum and average are {max(a)} and {sum(a)/len(a):.5f} and length is {len(Q)}\n")
		print(sorted(Counter(a).items()))
		print(f"Revised maximum and average lengths are {max(b)} and {sum(b)/len(b):.5f}")
		print(sorted(Counter(b).items()))
		with open("C:/Users/scho1/QTableMCTS/QTable-190.txt","w") as handler:
			json.dump(Q,handler) 
		handler.close()    

	def viewer():
		#Simple method of viewing Q table without amendments
		Q = []
		a = []	
		b = []
		minimumIteration = 88
		counter = 0
		kept = 0
		if (os.path.isfile('C:/Users/scho1/QTableMCTS/QTable.txt') == True):
			with open("C:/Users/scho1/QTableMCTS/QTable.txt", "r") as QTablefile:
				Q = json.load(QTablefile)
				print(f"Q-table uploaded with {len(Q)} lines")
		for item in Q:
			length = len(item[0])
			a.append(length)
			b.append(item[1])
		print(f"Maximum and average iterations are {max(a)} and {sum(a)/len(a):.5f}")
		print(sorted(Counter(a).items()))
		a.clear()
		print(f"Maximum and average lengths are {max(b)} and {sum(b)/len(b):.5f}")
		print(sorted(Counter(b).items()))
		b.clear()

	def massedit(iteration):
		Q = []
		counter = 0
		if (os.path.isfile('C:/Users/scho1/QTableMCTS/QTable.txt') == True):
			with open("C:/Users/scho1/QTableMCTS/QTable.txt", "r") as QTablefile:
				Q = json.load(QTablefile)
				print(f"Q-table uploaded with {len(Q)} lines")
		for item in Q.copy():
			if (len(item[0]) == iteration and item[2] > 0):
				item[2] = 0
				counter = counter + 1
		print(f"Number of items amended to length 0 for iteration {iteration} was {counter}")
		with open("C:/Users/scho1/QTableMCTS/QTable.txt","w") as handler:
			json.dump(Q,handler) 
		handler.close()    

	def reader(iteration,min,entries,start = ""):
		Q = []
		sum = 0
		minimum = min
		verbose = entries
		QDictLength = {}
		QDictVisits = {}
		if (os.path.isfile('C:/Users/scho1/QTableMCTS/QTable.txt') == True and Q == []):
			with open("C:/Users/scho1/QTableMCTS/QTable.txt", "r") as QTablefile:
				Q = json.load(QTablefile)
				print(f"Q Table uploaded with {len(Q)} lines")
		for item in Q:
			length = len(item[0])
			if (length == iteration and item[1] >= minimum and str(item[0]).startswith(start)):
				QDictLength[str(item[0])] = item[1] # 1 for iteration and 2 for visit
				QDictVisits[str(item[0])] = item[2]
				sum += 1
		print(f"Entries which are {minimum} or more of length {iteration} are {sum}")
		if verbose == True:
			entries = sorted(QDictLength.items(), key=lambda x: x[1], reverse=True)
			for element in entries:			
				print(f"{element[0]}, {element[1]}, {QDictVisits[element[0]]}")

	def rangeReader(begin, end, min,entries,start = ""):
		Q = []
		sum = 0
		minimum = min
		verbose = entries
		QDictLength = {}
		QDictVisits = {}
		if (os.path.isfile('C:/Users/scho1/QTableMCTS/QTable.txt') == True and Q == []):
			with open("C:/Users/scho1/QTableMCTS/QTable.txt", "r") as QTablefile:
				Q = json.load(QTablefile)
				print(f"Q Table uploaded with {len(Q)} lines")
		for iteration in range(begin,end):
			for item in Q:
				length = len(item[0])
				if (length == iteration and item[1] >= minimum and str(item[0]).startswith(start)):
					QDictLength[str(item[0])] = item[1] # 1 for iteration and 2 for visit
					QDictVisits[str(item[0])] = item[2]
					sum += 1
			print(f"Entries which are {minimum} or more of length {iteration} are {sum}")
			if verbose == True:
				entries = sorted(QDictLength.items(), key=lambda x: x[1], reverse=True)
				for element in entries:			
					print(f"{element[0]}, {element[1]}, {QDictVisits[element[0]]}")
			QDictLength = {}
			QDictVisits = {}
			sum = 0

	# Extract information on sample size, iteration and then "shortened" info
	def runParser(size, cutoff, length, useMin, minimum):	
		count1 = 0
		count2 = 0
		newmin = 0
		compact = list()
		cnt1 = Counter() # initial iterations 
		cnt2 = Counter() # final 
		cnt3 = Counter() # time taken
		cnt4 = Counter() # count for final iteration
		cnt5 = Counter() # iterations skipped through greedy runs
		cnt6 = Counter() # number of (remaining) viable iterations
		comment = "" # classify what sequence the match falls under
		if (os.path.isfile('MCTSRunSummary.txt') == True):
			with open("MCTSRunSummary.txt","r") as file:
				line = file.readline()		
				while line != "":	
					if line.startswith("["):
						# normally 60 but can be lengthened
						fullmatch = line #used with starts with function to avoid length affecting cutoff
						match = line[:length]
					if line.startswith("The lookahead"):
						count1 += 1
						file.readline()
						file.readline()
						nextline = file.readline()
						if nextline.startswith("Shortened"):
							compact.append(int(line[49:50]))
							if line[68] == "w":							
								compact.append(int(line[60:68]))
							else:
								compact.append(int(line[60:68]))
							shortlist = nextline[16:].split()
							compact.append(int(shortlist[0]))
							compact.append(float(shortlist[1]))
							compact.append(int(shortlist[2]))
							compact.append(int(shortlist[3]))
							next = file.readline()
							if next.startswith("Long"):
								longlist = next[0:].split()
								compact.append(int(longlist[8]))
								compact.append(int(longlist[9]))
								# Capturing number of viable iterations if these exist
								if len(longlist) > 10:
									compact.append(int(longlist[10]))
							# Specific to longest iterations
							if (fullmatch.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60, 35, 58, 51, 3, 56, 160, 131, 192, 126, 179, 138, 66, 196, 134, 108, 120, 230, 130, 63, 27, 23")):
								comment = "213 Sequence: 5 11 ... 58 51 3 ... 230 130 63 27 23 NEW AREA"
								newmin = 0
							elif (fullmatch.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60, 35, 58, 51, 3, 56, 160, 131, 192, 126, 179, 138, 66, 196, 134, 108, 120, 230, 130, 63, 27")):
								comment = "213 Sequence: 5 11 ... 58 51 3 ... 120 230 130 63 27 min 194"
								newmin = 194
							elif (fullmatch.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60, 35, 58, 51, 3, 56, 160, 131, 192, 126, 179, 138, 66, 196, 134, 108, 120, 230, 130, 63, 26")):
								comment = "213 Sequence: 5 11 ... 58 51 3 ... 120 230 130 63 26 min 202"
								newmin = 202
							elif (fullmatch.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60, 35, 58, 51, 3, 56, 160, 131, 192, 126, 179, 138, 66, 196, 134, 108, 120, 230, 253")):
								comment = "213 Sequence: 5 11 ... 58 51 3 ... 134 108 120 230 253 min 207"
								newmin = 207
							elif (fullmatch.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60, 35, 58, 51, 3, 56, 160, 131, 192, 126, 179, 138, 66, 196, 134, 108")):
								comment = "213 Sequence: 5 11 ... 58 51 3 ... 138 66 196 134 108 min 203"
								newmin = 203
							elif (fullmatch.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60, 35, 58, 51, 3, 56, 160, 131, 192, 126, 179, 138, 66, 196, 134, 175")):
								comment = "213 Sequence: 5 11 ... 58 51 3 ... 138 66 196 134 175 min 207"
								newmin = 207
							elif (fullmatch.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60, 35, 58, 51, 3, 56, 160, 131, 192, 126, 179, 138, 66, 196")):
								comment = "213 Sequence: 5 11 ... 58 51 3 ... 126 179 138 66 196 min 203"
								newmin = 203
							elif (fullmatch.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60, 35, 58, 51, 3, 56, 160, 131, 192, 126, 179, 138")):
								comment = "213 Sequence: 5 11 ... 58 51 3 ... 126 179 138 min 205"
								newmin = 205
							elif (fullmatch.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60, 35, 58, 51, 3, 56, 160, 131, 192, 126, 179, 140")):
								comment = "213 Sequence: 5 11 ... 58 51 3 ... 126 179 140 min 207"
								newmin = 207
							elif (fullmatch.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60, 35, 58, 51, 3, 56, 160, 131, 192, 126")):
								comment = "213 Sequence: 5 11 ... 58 51 3 ... 126 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60, 35, 58, 51, 3, 56, 160, 131, 192")):
								comment = "213 Sequence: 5 11 ... 58 51 3 56 160 131 192 min 207"
								newmin = 207
							elif (fullmatch.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60, 35, 58, 51, 3, 56, 160, 131")):
								comment = "213 Sequence: 5 11 ... 58 51 3 56 160 131 min 205"
								newmin = 205	
							elif (fullmatch.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60, 35, 58, 51, 3, 56, 160, 132")):
								comment = "213 Sequence: 5 11 ... 58 51 3 56 160 132 min 208"
								newmin = 208
							elif (match.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60, 35, 58, 51, 3")):
								comment = "213 Sequence: 5 11 ... 58 51 3 min 207"
								newmin = 207
							elif (match.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60, 35, 58")):
								comment = "213 Sequence: 5 11 ... 58 min 207"
								newmin = 207
							elif (match.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60, 35, 56")):
								comment = "213 Sequence: 5 11 ... 56 min 204"
								newmin = 204
							elif (match.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60, 35")):
								comment = "213 Sequence: 5 11 15 8 60 35 min 205"
								newmin = 205
							elif (match.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60")):
								comment = "213 Sequence: 5 11 15 8 60 min 205"
								newmin = 205
							elif (match.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8")):
								comment = "213 Sequence: 5 11 15 8 min 205"
								newmin = 205
							elif (match.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11, 15")):
								comment = "213 Sequence: 5 11 15 min 206"
								newmin = 206
							elif (match.startswith("[4, 16, 28, 31, 25, 13, 52, 5, 11")):
								comment = "213 Sequence: 5 11 min 205"
								newmin = 205
							elif (match.startswith("[4, 16, 28, 31, 25, 13, 52, 5")):
								comment = "213 Sequence: 5 min 205"
								newmin = 205
							elif (match.startswith("[4, 16, 28, 31, 25, 13, 52")):
								comment = "213 Sequence: Early 4 16 28 31 25 13 52 min 206"
								newmin = 206
							elif (match.startswith("[4, 16, 28, 31, 25, 13, 56")):
								comment = "213 Sequence: Early 4 16 28 31 25 13 56 min 204"
								newmin = 204
							elif (match.startswith("[4, 16, 28, 31, 25, 13")):
								comment = "213 Sequence: Early 4 16 28 31 25 13 min 205"
								newmin = 205
							elif (match.startswith("[4, 16, 28, 31, 25")):
								comment = "213 Sequence: Early 4 16 28 31 25 min 206"
								newmin = 206
							elif (match.startswith("[4, 16, 28, 31")):
								comment = "213 Sequence: Early 4 16 28 31 min 206"
								newmin = 206
							elif (match.startswith("[4, 16, 28")):
								comment = "213 Sequence: Early 4 16 28 min 206"
								newmin = 206
							elif (match.startswith("[4, 16")):
								comment = "213 Sequence: Early 4 16 min 205"
								newmin = 205
							elif (match.startswith("[4, 21")):
								comment = "213 Sequence: Early 4 21 min 204"
								newmin = 204
							elif (match.startswith("[4")):
								comment = "213 Sequence: Early 4 min 205"
								newmin = 205
							else:
								comment = "213 Sequence: Non 4"
								newmin = 0
							if (useMin == True):
								if ((compact[2]>=cutoff or compact[4]>=cutoff) and count2 >= minimum and (compact[2]>=newmin or compact[4]>=newmin)):
									print(f"{match}] {compact} {comment}")
							else:
								if ((compact[2]>=cutoff or compact[4]>=cutoff) and count2 >= minimum):
									print(f"{match}] {compact} {comment}")
							count2 += 1
						else:
							count1 = 0
						if size in compact:
							cnt1[compact[2]] += 1
							cnt2[compact[4]] += 1
							# May need tuning for higher iterations - set at 1 hr at present
							if (size == 300000):
								timing = 3600
							elif (size == 350000):
								timing = 4100
							elif (size > 350000):
								timing = 1000
							if compact[5] < timing:
								cnt3[compact[5]] += 1									
							if (len(compact) > 6):
								cnt4[compact[6]] += 1
								cnt5[compact[7]] += 1
								if (len(compact) > 8):
									cnt6[compact[8]] += 1			
					compact.clear()
					comment = ""
					line = file.readline()						
			if (count1 != count2):
				print("ERROR: Mismatch of counts between lookahead and shortened text lines")
			print(f"There are {count1} shortened entries in the file with up to {count1-minimum} shown above")
			print(f"The counter of iteration values for {size} had an average of {sum(cnt1.elements())/sum(cnt1.values()):.2f} for {sum(cnt1.values())} runs and was:\n {sorted(cnt1.items())}")
			print(f"The counter of final values for {size} had an average of {sum(cnt2.elements())/sum(cnt2.values()):.2f} for {sum(cnt2.values())} runs and was:\n {sorted(cnt2.items())}")
			print(f"Long Form Information: The length of the final iteration (normally 5m) for {sum(cnt4.values())} runs was :\n {sorted(cnt4.items())}")
			print(f"Long Form Information: The number of greedy iterations skipped had an average of {sum(cnt5.elements())/sum(cnt5.values()):.2f} for {sum(cnt5.values())} runs:\n {sorted(cnt5.items())}")
			print(f"Long Form Information: The number of remaining viable iterations had an average of {sum(cnt6.elements())/sum(cnt6.values()):.2f} for {sum(cnt6.values())} runs:\n{sorted(cnt6.items())}")
			print(f"Time to Complete: There were {sum(cnt3.values())} entries less than {timing} seconds and the average was {sum(cnt3.elements())/sum(cnt3.values()):.2f}")

			file.close()

	def table(min):
		Q = []
		sum = 0
		minimum = min
		output = ""
		QDictLength = {}
		QDictVisits = {}
		if (os.path.isfile('C:/Users/scho1/QTableMCTS/QTable.txt') == True):
			with open("C:/Users/scho1/QTableMCTS/QTable.txt", "r") as QTablefile:
				Q = json.load(QTablefile)
				print(f"Q Table uploaded with {len(Q)} lines")
		print(f"Entries which are {minimum} or more for iterations 1 to 6:")
		for iteration in range(1,7):
			for item in Q:
				length = len(item[0])
				if (length == iteration and item[1] >= minimum):
					QDictLength[str(item[0])] = item[1] # 1 for iteration and 2 for visit
					QDictVisits[str(item[0])] = item[2]
					sum += 1
			output += str(sum) + " "
			sum = 0
		print (output)
		#for i in range(1,6):
		#	QCleanup.reader(i, min, False)

	def updateFrom88():
		Q = []
		itemList = []
		updateList = []
		textInput = ""
		errorNote = False
		if (os.path.isfile('C:/Users/scho1/QTableMCTS/QTable.txt') == True):
			with open("C:/Users/scho1/QTableMCTS/QTable.txt", "r") as QTablefile:
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
		with open("C:/Users/scho1/QTableMCTS/QTable.txt","w") as handler:
			json.dump(Q,handler) 
		handler.close()  
		
	# Input is received from user for cutoff and viable iterations
	def iterationReader():
		# Note that it seems hard to store integer keys in the Counter and by default these are txt in json
		# Could only store dictionary rather than list but it would take too many files
		dist = [] # list containing cutoff and Counter for lengths of viable options
		storedCntr = Counter() # Counter for a particular cutoff
		itemFound = False # Check to see if counter has been stored for this iteration
		textInput = 0
		if (os.path.isfile('Count-Distribution.txt') == True):
			with open("Count-Distribution.txt", "r") as CountDistributionfile:
				dist = json.load(CountDistributionfile)
			print(f"Count distribution uploaded with {len(dist)} entries")
		textInput1 = int(input("Enter the cutoff used for this iteration (in millions): "))
		textInput1 = textInput1*1000000
		for item in dist:
			if textInput1 == item[0]:
				storedCntr = item[1]
				print(f"Initial counter for cutoff {textInput1} uploaded as: \n{sorted(storedCntr.items())}")
				itemFound = True
		if (itemFound == False):
			print(f"No initial count distribution was found")
		textInput2 = input("Enter the list of viable iterations (including brackets): ")
		textInput2 = textInput2[1:-1]
		itemList = [int(item) for item in textInput2.split(',')]
		textItemList = [str(item).strip() for item in textInput2.split(',')]
		counter = Counter(itemList)
		textCounter = Counter(textItemList) # seems incredibly hard to store Counter as int keys
		print(f"The counter for this particular iteration was {sorted(counter.items())}")
		length = len(itemList)
		average = sum(itemList)/length
		print(f"There were {len(itemList)} viable options with an average of {average:.3f}")
		storedCntr = Counter(storedCntr) + Counter(textCounter)
		itemFound = False
		for item in dist:
			if textInput1 == item[0]:
				item[1] = storedCntr
				print(f"The stored counter has been updated to: \n{sorted(storedCntr.items())}")
				itemFound = True
		if (itemFound == False):
			dist.append([textInput1,storedCntr]) # difficulty in ensuring this is int rather than txt
			print(f"A new stored counter has been created of :\n{sorted(storedCntr.items())}")
		print(f"The total count was {sum(storedCntr.values())} and the 5 most common values were {storedCntr.most_common(5)}")
		with open("Count-Distribution.txt","w") as handler:
			json.dump(dist,handler)
		handler.close()

	# Input is read from main file
	def viableIterations(cutoff, currentdist):
		storedCntr = Counter() # Counter for a particular cutoff
		dist = [] # list containing cutoff and Counter for lengths of viable options
		itemFound = False
		if (os.path.isfile('Count-Distribution.txt') == True):
			with open("Count-Distribution.txt", "r") as CountDistributionfile:
				dist = json.load(CountDistributionfile)
			print(f"Count distribution uploaded with {len(dist)} entries")
		for item in dist:
			if cutoff == item[0]:
				storedCntr = item[1]
				print(f"Initial counter for cutoff {cutoff} uploaded as: \n{sorted(storedCntr.items())}")
				itemFound = True
		if (itemFound == False):
			print(f"No initial count distribution was found for cutoff {cutoff}")
		textItemList = [str(item) for item in currentdist]
		length = len(currentdist)
		average = sum(currentdist)/length
		print(f"There were {length} viable options with an average of {average:.3f}")
		textCounter = Counter(textItemList) # seems incredibly hard to store Counter as int keys		
		storedCntr = Counter(storedCntr) + Counter(textCounter)
		itemFound = False
		for item in dist:
			if cutoff == item[0]:
				item[1] = storedCntr
				print(f"The stored counter has been updated to: \n{sorted(storedCntr.items())}")
				itemFound = True
		if (itemFound == False):
			dist.append([cutoff,storedCntr]) # difficulty in ensuring this is int rather than txt
			print(f"A new stored counter has been created of :\n{sorted(storedCntr.items())}")
		print(f"The total count was {sum(storedCntr.values())} and the 3 most common values were {storedCntr.most_common(3)}")
		with open("Count-Distribution.txt","w") as handler:
			json.dump(dist,handler)
		handler.close()
		return length # output number of viable options

	def viewCounter(cutoff):
		if (os.path.isfile('Count-Distribution.txt') == True):
			with open("Count-Distribution.txt", "r") as CountDistributionfile:
				dist = json.load(CountDistributionfile)
			print(f"Count distribution uploaded with {len(dist)} entries")
		for item in dist:
			if cutoff == item[0]:
				storedCntr = item[1]
				print(f"Counter for cutoff {cutoff} uploaded as: \n{sorted(storedCntr.items())}")
				itemFound = True
		if (itemFound == False):
			print(f"No initial count distribution was found for cutoff {cutoff}")
		storedCntr = Counter(storedCntr)
		print(f"The total count was {sum(storedCntr.values())} and the 3 most common values were {storedCntr.most_common(3)}")

	def Fib(n):
		if n <= 2:
			return 1
		else:
			return QCleanup.Fib(n-1) + QCleanup.Fib(n-2)

	#Example of memoization
	def FibMemo(n, memo = {}):
		if n in memo:
			return memo[n]
		if n <= 2:
			return 1
		memo[n] = QCleanup.FibMemo(n - 1, memo) + QCleanup.FibMemo(n - 2, memo) 
		# Question is whether it's n-1, memo or just n-1...
		print(f"memo {n} is {memo[n]}")
		return memo[n]
	#Memoization is amazing!!!!!

	def canSum( targetSum, numbers):
		if targetSum == 0:
			return True
		if targetSum < 0:
			return False

		for num in numbers:
			remainder = targetSum - num
			if QCleanup.canSum(remainder, numbers) == True:
				return True

		return False

	def canSumMemo( targetSum, numbers, memo = {}):
		if targetSum in memo:
			return memo[targetSum]
		if targetSum == 0:
			return True
		if targetSum < 0:
			return False

		for num in numbers:
			remainder = targetSum - num
			if QCleanup.canSumMemo(remainder, numbers, memo) == True:
				memo[remainder] = True
				print(f"memo {remainder} is {memo[remainder]}")
				return memo[remainder]
		
		memo[remainder] = False
		print(f"memo {remainder} is {memo[remainder]}")
		return memo[remainder]

	def allConstruct(target, wordBank):
		result = []		
		if target == "":
			return [[]]
		for word in wordBank:
			if target.startswith(word) == True:
				suffix = target.replace(word,"")
				suffixWays = QCleanup.allConstruct(suffix, wordBank)
				for item in suffixWays:
					item.insert(0,word)
				result.extend(suffixWays)
		return result

QCleanup.rangeReader(0,35,209,True)
#QCleanup.reader(34,1,True,"[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60, 35, 58, 51, 3, 56, 160, 131, 192, 126, 179, 138, 66, 196, 134, 108, 120, 230, 130, 63, 27, 23")
#QCleanup.reader(24,1,True,"[4, 16, 28, 31, 25, 13, 52, 5, 11, 15, 8, 60, 35, 58, 51, 3, 56, 160, 131, 192, 126, 179, 138")
#QCleanup.reader(88,205,True)
#QCleanup.reader(3,1,True,"[2, 39")
#QCleanup.viewer()
#QCleanup.table(180)
#QCleanup.viewCounter(400000)
# True indicates using new minimum function which only shows iterations that need updating
#QCleanup.runParser(500000,1,139,True,10293) 
