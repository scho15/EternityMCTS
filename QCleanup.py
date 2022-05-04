import json
import os.path
from collections import Counter

class QCleanup:
	# Simple file to read Q and see if any entries exceed 88 (and Q can be "dumped" back in edited form)
	# Could use later to sort through Q and see some interesting properties
	def cleanser(cutoff, minimumIteration):
		Q = []
		a = []	
		b = []
		#cutoff = 200
		#minimumIteration = 6
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
		print(f"\nIntroducing a minimum cutoff of {cutoff} for iterations greater than length {minimumIteration}")
		for item in Q.copy():
			if (item[1] < cutoff and len(item[0]) > minimumIteration):
				Q.remove(item)				
				counter += 1
				if (counter%10000 == 0):
					print(f"{counter} items have been removed and items kept is {kept}")
			else:
				kept += 1
				#item[2] = 0 # Only used for 205 reset
		for item in Q:
			length = len(item[0])
			a.append(length)
			b.append(item[1])
		print(f"Revised maximum and average are {max(a)} and {sum(a)/len(a):.5f} and length is {len(Q)}\n")
		print(sorted(Counter(a).items()))
		print(f"Revised maximum and average lengths are {max(b)} and {sum(b)/len(b):.5f}")
		print(sorted(Counter(b).items()))
		with open("C:/Users/scho1/QTableMCTS/QTable-200.txt","w") as handler:
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

	def qCombine():
		identical = 0
		different = 0
		found = False
		Q1 = []
		Q2 = []
		location1 = 'C:/Users/scho1/QTableMCTS/Run 1/QTableCombined.txt'
		location2 = 'C:/Users/scho1/QTableMCTS/Run 4/QTableFINALRun4.txt'
		Q1 = QCleanup.qTableViewer(location1)
		Q2 = QCleanup.qTableViewer(location2)
		for item2 in Q2.copy():
			for item1 in Q1.copy():
				if (item1[0] == item2[0]):
					identical += 1
					found = True
					print(f"{item1[0]} appears in both tables with maxes {item1[1]} and {item2[1]}")
					item1[1] = max(item1[1],item2[1])
			if (found == False):
				different += 1	
				Q1.append(item2)
				if (different%1000 == 0):
					print(f"{different} items appended")
			found = False
		print(f"The Q Tables had {identical} matches and {different} items not found")
		a = []	
		b = []
		for item in Q1:
			length = len(item[0])
			a.append(length)
			b.append(item[1])
		print(f"Maximum and average iterations are now {max(a)} and {sum(a)/len(a):.5f}")
		print(sorted(Counter(a).items()))
		a.clear()
		print(f"Maximum and average lengths are now {max(b)} and {sum(b)/len(b):.5f}")
		print(sorted(Counter(b).items()))
		b.clear()
		with open("C:/Users/scho1/QTableMCTS/Run 1/QTableNEWCombined.txt","w") as handler:
			json.dump(Q1,handler) 
		handler.close()   

	def qTableViewer(fileLoc):
		#Simple method of viewing Q table without amendments
		Q = []
		a = []	
		b = []
		counter = 0
		if (os.path.isfile(fileLoc) == True):
			with open(fileLoc, "r") as QTablefile:
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
		return Q

	# Amended to change counter to 6000 from 5979 as one off
	def massedit():
		Q = []
		counter = 0
		if (os.path.isfile('C:/Users/scho1/QTableMCTS/QTable.txt') == True):
			with open("C:/Users/scho1/QTableMCTS/QTable.txt", "r") as QTablefile:
				Q = json.load(QTablefile)
				print(f"Q-table uploaded with {len(Q)} lines")
		for item in Q.copy():
			if (len(item[0]) == 0 and item[2] == 5979):
				item[2] = 6000
		with open("C:/Users/scho1/QTableMCTS/QTable.txt","w") as handler:
			json.dump(Q,handler) 
		handler.close()    

	def reader(iteration,min,entries,start = "",loc = 'C:/Users/scho1/QTableMCTS/QTable.txt'):
		Q = []
		sum = 0
		minimum = min
		verbose = entries
		QDictLength = {}
		QDictVisits = {}
		if (os.path.isfile(loc) == True and Q == []):
			with open(loc, "r") as QTablefile:
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
		if (os.path.isfile('C:/Users/scho1/QTableMCTS/MCTSRunSummary.txt') == True):
			with open("C:/Users/scho1/QTableMCTS/MCTSRunSummary.txt","r") as file:
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
							if (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149, 173, 141, 25, 22, 85, 205, 161, 217, 74, 168, 170, 234, 176, 166, 129, 135, 248, 237")):
								comment = "64: 4 18...166 129 135 248 237 NEW AREA"
								newmin = 0
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149, 173, 141, 25, 22, 85, 205, 161, 217, 74, 168, 170, 234, 176, 166, 129, 135, 248")):
								comment = "63: 4 18...176 166 129 135 248 min 203"
								newmin = 203
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149, 173, 141, 25, 22, 85, 205, 161, 217, 74, 168, 170, 234, 176, 166")):
								comment = "60: 4 18...168 170 234 176 166 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149, 173, 141, 25, 22, 85, 205, 161, 217, 74, 168, 170, 234")):
								comment = "58: 4 18...217 74 168 170 234 min 205"
								newmin = 205
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149, 173, 141, 25, 22, 85, 205, 161, 217, 74, 168, 170")):
								comment = "57: 4 18...161 217 74 168 170 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149, 173, 141, 25, 22, 85, 205, 161, 217, 74, 168")):
								comment = "56: 4 18...205 161 217 74 168 min 207"
								newmin = 207
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149, 173, 141, 25, 22, 85, 205, 161, 217")):
								comment = "54: 4 18...22 85 205 161 217 min 205"
								newmin = 205
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149, 173, 141, 25, 22, 85, 148")):
								comment = "51+: 4 18...173 141 25 22 85 + 148 min 204"
								newmin = 204
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149, 173, 141, 25, 22, 85")):
								comment = "51: 4 18...173 141 25 22 85 min 208"
								newmin = 208
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149, 173, 141, 25, 22")):
								comment = "50: 4 18...149 173 141 25 22 min 205"
								newmin = 205
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149, 173, 141, 25, 52")):
								comment = "49+: 4 18...154 149 173 141 25 + 52 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149, 173, 141, 25, 24")):
								comment = "49+: 4 18...154 149 173 141 25 + 24 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149, 173, 141, 25, 37")):
								comment = "49+: 4 18...154 149 173 141 25 + 37 min 203"
								newmin = 203
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149, 173, 141, 25, 5,")):
								comment = "49+: 4 18...154 149 173 141 25 + 5 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149, 173, 141, 25")):
								comment = "49: 4 18...154 149 173 141 25 min 207"
								newmin = 207
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149, 173, 144")):
								comment = "47+: 4 18...111 120 154 149 173 + 144 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149, 173")):
								comment = "47: 4 18...111 120 154 149 173 min 207"
								newmin = 207
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149")):
								comment = "46: 4 18...127 111 120 154 149 min 208"
								newmin = 208
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154")):
								comment = "45: 4 18...106 127 111 120 154 min 211"
								newmin = 211
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120")):
								comment = "44: 4 18...200 106 127 111 120 min 207"
								newmin = 207
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138")):
								comment = "38: 4 18...14 88 214 140 138 min 207"
								newmin = 207
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214")):
								comment = "36: 4 18...81 26 14 88 214 min 211"
								newmin = 211
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88")):
								comment = "35: 4 18...240 81 26 14 88 min 207"
								newmin = 207
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14")):
								comment = "34: 4 18...194 240 81 26 14 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 10")):
								comment = "33+: 4 18...193 194 240 81 26 + 10 min 205"
								newmin = 205
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 54")):
								comment = "33+: 4 18...193 194 240 81 26 + 54 min 205"
								newmin = 205
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26")):
								comment = "33: 4 18...193 194 240 81 26 min 207"
								newmin = 207
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102")):
								comment = "27: 4 18...180 162 89 104 102 min 207"
								newmin = 207
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104")):
								comment = "26: 4 18...122 180 162 89 104 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89")):
								comment = "25: 4 18...131 122 180 162 89 min 207"
								newmin = 207
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162")):
								comment = "24: 4 18...118 131 122 180 162 min 208"
								newmin = 208
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180")):
								comment = "23: 4 18...77 118 131 122 180 min 208"
								newmin = 208
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122")):
								comment = "22: 4 18...44 77 118 131 122 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131")):
								comment = "21: 4 18...3 44 77 118 131 min 207"
								newmin = 207
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118")):
								comment = "20: 4 18...31 3 44 77 118 min 211"
								newmin = 211
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44")):
								comment = "18: 4 18...9 32 31 3 44 min 206"
								newmin = 207
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3")):
								comment = "17: 4 18...45 9 32 31 3 min 208"
								newmin = 208
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32")):
								comment = "15: 4 18...35 53 45 9 32 min 207"
								newmin = 207
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 34")):
								comment = "14+: 4 18...28 35 53 45 9 + 34 min 205"
								newmin = 205
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 26")):
								comment = "14+: 4 18...28 35 53 45 9 + 26 min 205"
								newmin = 205
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 29")):
								comment = "14+: 4 18...28 35 53 45 9 + 29 min 205"
								newmin = 205
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9")):
								comment = "14: 4 18...28 35 53 45 9 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 5")):
								comment = "13+: 4 18...27 28 35 53 45 + 5 min 205"
								newmin = 205
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45")):
								comment = "13: 4 18...27 28 35 53 45 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53")):
								comment = "12: 4 18...16 27 28 35 53 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 50")):
								comment = "11+: 4 18...19 16 27 28 35 + 50 min 205"
								newmin = 205
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 52")):
								comment = "11+: 4 18...19 16 27 28 35 + 52 min 205"
								newmin = 205
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28, 35")):
								comment = "11: 4 18...19 16 27 28 35 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 28")):
								comment = "10: 4 15...6 19 16 27 28 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 30")):
								comment = "9+: 4 15...15 6 19 16 27 + 30 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27, 35")):
								comment = "9+: 4 15...15 6 19 16 27 + 35 min 205"
								newmin = 205
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16, 27")):
								comment = "9: 4 15...15 6 19 16 27 min 207"
								newmin = 207
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 16")):
								comment = "8: 4 18 51 15 6 19 16 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19, 20")):
								comment = "7+: 4 18 51 15 6 19 + 20 min 205"
								newmin = 205
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 19")):
								comment = "7: 4 18 51 15 6 19 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18, 51, 15, 6, 20")):
								comment = "6+: 4 18 51 15 6 + 20 min 205"
								newmin = 205
							elif (fullmatch.startswith("[4, 18, 51, 15, 6")):
								comment = "6: 4 18 51 15 6 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18, 51, 15, 7")):
								comment = "5+: 4 18 51 15 + 7 min 205"
								newmin = 205
							elif (fullmatch.startswith("[4, 18, 51, 15")):
								comment = "5: 4 18 51 15 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18, 51, 23")):
								comment = "4+: 4 18 51 + 23 min 205"
								newmin = 205
							elif (fullmatch.startswith("[4, 18, 51")):
								comment = "4: 4 18 51 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 18")):
								comment = "3: 4 18 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4, 25")):
								comment = "2+: 4 + 25 min 205"
								newmin = 205
							elif (fullmatch.startswith("[4, 19")):
								comment = "2+: 4 + 19 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4")):
								comment = "2: 4 min 207"
								newmin = 207
							elif (fullmatch.startswith("[1, 27")):
								comment = "Non 4: 1 27 min 204"
								newmin = 204
							elif (fullmatch.startswith("[1, 34")):
								comment = "Non 4: 1 34 min 204"
								newmin = 204
							elif (fullmatch.startswith("[1, 26")):
								comment = "Non 4: 1 26 min 203"
								newmin = 203
							elif (fullmatch.startswith("[1, 26")):
								comment = "Non 4: 1 35 min 203"
								newmin = 203
							elif (fullmatch.startswith("[1")):
								comment = "Non 4: 1 min 205"
								newmin = 205
							elif (fullmatch.startswith("[2, 45")):
								comment = "Non 4: 2 45 min 203"
								newmin = 203
							elif (fullmatch.startswith("[2, 47")):
								comment = "Non 4: 2 47 min 203"
								newmin = 203
							elif (fullmatch.startswith("[2")):
								comment = "Non 4: 2 min 204"
								newmin = 204
							elif (fullmatch.startswith("[3, 36")):
								comment = "Non 4: 3 36 min 203"
								newmin = 203
							elif (fullmatch.startswith("[3")):
								comment = "Non 4: 3 min 204"
								newmin = 204
							elif (fullmatch.startswith("[")):
								comment = "Error - should not reach this statement"
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
							elif (size > 350000 and size < 750000):
								timing = 1000
							elif (size >= 750000):
								timing = 1200
							if compact[5] < timing:
								cnt3[compact[5]] += 1									
							if (len(compact) > 6):
								# summarised final iteration into buckets of 1m
								cnt4[int(compact[6]/1000000)] += 1
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
			print(f"Long Form Information: The length of the final iteration (normally 20x) for {sum(cnt4.values())} runs was :\n {sorted(cnt4.items())}")
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

	# Can be used to insert newly found solution with max being length of solution
	def updateFrom96(max):
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
		updateList = itemList.copy()[:96]
		while(len(updateList) > 0):
			itemFound = False
			for item in Q:
				if updateList == item[0]:
					item[1] = max
					item[2] = item[2] + 1
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
		with open("C:/Users/scho1/QTableMCTS/QTableTemp.txt","w") as handler:
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
		if (os.path.isfile('C:/Users/scho1/QTableMCTS/Count-Distribution.txt') == True):
			with open("C:/Users/scho1/QTableMCTS/Count-Distribution.txt", "r") as CountDistributionfile:
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
		with open("C:/Users/scho1/QTableMCTS/Count-Distribution.txt","w") as handler:
			json.dump(dist,handler)
		handler.close()

	# Input is read from main file
	def viableIterations(cutoff, currentdist):
		storedCntr = Counter() # Counter for a particular cutoff
		dist = [] # list containing cutoff and Counter for lengths of viable options
		itemFound = False
		if (os.path.isfile('C:/Users/scho1/QTableMCTS/Count-Distribution.txt') == True):
			with open("C:/Users/scho1/QTableMCTS/Count-Distribution.txt", "r") as CountDistributionfile:
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
		if length != 0:
			average = sum(currentdist)/length
			print(f"There were {length} viable options with an average of {average:.3f}")
		else:
			print(f"The run was completed with any samples being taken")
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
		with open("C:/Users/scho1/QTableMCTS/Count-Distribution.txt","w") as handler:
			json.dump(dist,handler)
		handler.close()
		return length # output number of viable options

	def viewCounter(cutoff):
		if (os.path.isfile('C:/Users/scho1/QTableMCTS/Count-Distribution.txt') == True):
			with open("C:/Users/scho1/QTableMCTS/Count-Distribution.txt", "r") as CountDistributionfile:
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

#QCleanup.cleanser(200, 6)
#QCleanup.qCombine() # Used very rarely!
#QCleanup.qTableViewer("C:/Users/scho1/QTableMCTS/Run 1/QTableFINALRun1.txt")
#QCleanup.reader(6,1,True,"[4, 18, 51, 15, 6","C:/Users/scho1/QTableMCTS/Run 1/QTableCombined.txt")
#Combination of runs 1,2 and 4 already has 430186 lines with 205 cutoff
#QCleanup.rangeReader(0,73,211,True)
#QCleanup.reader(96,205,True)
#QCleanup.reader(65,1,True,"[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149, 173, 141, 25, 22, 85, 205, 161, 217, 74, 168, 170, 234, 176, 166, 129, 135, 248, 237, 11")
#QCleanup.reader(60,1,True,"[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104, 102, 115, 193, 194, 240, 81, 26, 14, 88, 214, 140, 138, 159, 200, 106, 127, 111, 120, 154, 149, 173, 141, 25, 22, 85, 205, 161, 217, 74, 168, 170, 234, 176, 166")
#QCleanup.reader(26,1,True,"[4, 18, 51, 15, 6, 19, 16, 27, 28, 35, 53, 45, 9, 32, 31, 3, 44, 77, 118, 131, 122, 180, 162, 89, 104")
#QCleanup.reader(11,1,True,"[4, 18, 51, 15, 6, 19, 16, 27, 28, 35")
#QCleanup.table(180)
#QCleanup.viewer()
#QCleanup.viewCounter(550000)
#QCleanup.updateFrom96(217)
# True indicates using new minimum function which only shows iterations that need updating
#QCleanup.runParser(550000,1,289,True,10000) 