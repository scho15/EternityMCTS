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
		#minimumIteration = 3
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
							if (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119, 182, 138, 219, 226, 123, 239, 36, 31, 108, 165, 212, 210, 83, 84, 64, 126, 168, 141")):
								comment = "60: 2 42 10 ... 84 64 126 168 141 NEW AREA"
								newmin = 0
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119, 182, 138, 219, 226, 123, 239, 36, 31, 108, 165, 212, 210, 83, 84, 64, 126, 168")):
								comment = "59: 2 42 10 ... 83 84 64 126 168 min 202"
								newmin = 202
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119, 182, 138, 219, 226, 123, 239, 36, 31, 108, 165, 212, 210, 83, 84, 64, 126")):
								comment = "58: 2 42 10 ... 210 83 84 64 126 min 205"
								newmin = 205
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119, 182, 138, 219, 226, 123, 239, 36, 31, 108, 165, 212, 210, 83, 84, 64")):
								comment = "57: 2 42 10 ... 212 210 83 84 64 min 207"
								newmin = 207
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119, 182, 138, 219, 226, 123, 239, 36, 31, 108, 165, 212, 210, 83, 84")):
								comment = "56: 2 42 10 ... 165 212 210 83 84 min 205"
								newmin = 205
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119, 182, 138, 219, 226, 123, 239, 36, 31, 108, 165, 212, 210")):
								comment = "54: 2 42 10 ... 31 108 165 212 210 min 210"
								newmin = 210
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119, 182, 138, 219, 226, 123, 239, 36, 31, 108, 165, 212")):
								comment = "53: 2 42 10 ... 36 31 108 165 212 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119, 182, 138, 219, 226, 123, 239, 36, 31, 108, 165, 211")):
								comment = "52: 2 42 10 ... 239 36 31 108 165 + 211 min 192"
								newmin = 192
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119, 182, 138, 219, 226, 123, 239, 36, 31, 108, 165, 209")):
								comment = "52: 2 42 10 ... 239 36 31 108 165 + 209 min 205"
								newmin = 205
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119, 182, 138, 219, 226, 123, 239, 36, 31, 108, 165")):
								comment = "52: 2 42 10 ... 239 36 31 108 165 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119, 182, 138, 219, 226, 123, 239, 36, 31, 108")):
								comment = "51: 2 42 10 ... 123 239 36 31 108 min 208"
								newmin = 208
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119, 182, 138, 219, 226, 123, 239, 36, 51")):
								comment = "49: 2 42 10 ... 219 226 123 239 36 + 51 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119, 182, 138, 219, 226, 123, 239, 36, 40")):
								comment = "49: 2 42 10 ... 219 226 123 239 36 + 40 min 205"
								newmin = 205
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119, 182, 138, 219, 226, 123, 239, 36, 19")):
								comment = "49: 2 42 10 ... 219 226 123 239 36 + 19 min 205"
								newmin = 205
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119, 182, 138, 219, 226, 123, 239, 36")):
								comment = "49: 2 42 10 ... 219 226 123 239 36 min 207"
								newmin = 207
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119, 182, 138, 219, 226")):
								comment = "46: 2 42 10 ... 119 182 138 219 226 min 207"
								newmin = 207
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119, 182, 138, 219")):
								comment = "45: 2 42 10 ... 85 119 182 138 219 min 207"
								newmin = 207
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119, 182")):
								comment = "43: 2 42 10 ... 248 203 85 119 182 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119")):
								comment = "42: 2 42 10 ... 77 248 203 85 119 min 208"
								newmin = 208
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85")):
								comment = "41: 2 42 10 ... 240 77 248 203 85 min 208"
								newmin = 208
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203")):
								comment = "40: 2 42 10 ... 249 240 77 248 203 min 207"
								newmin = 207
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 132")):
								comment = "39: 2 42 10 ... 249 240 77 248 + 132 min 201"
								newmin = 201
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248")):
								comment = "39: 2 42 10 ... 237 249 240 77 248 min 208"
								newmin = 208
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77")):
								comment = "38: 2 42 10 ... 18 237 249 240 77 min 208"
								newmin = 208
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240")):
								comment = "37: 2 42 10 ... 16 18 237 249 240 min 211"
								newmin = 211
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237")):
								comment = "35: 2 42 10 ... 192 81 16 18 237 min 208"
								newmin = 208
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 55")):
								comment = "33: 2 42 10 ... 235 244 192 81 16 + 55 min 205"
								newmin = 205
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 39")):
								comment = "33: 2 42 10 ... 235 244 192 81 16 + 39 min 205"
								newmin = 205
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16")):
								comment = "33: 2 42 10 ... 235 244 192 81 16 min 207"
								newmin = 207
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151")):
								comment = "28: 2 42 10 ... 247 104 127 206 151 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206")):
								comment = "27: 2 42 10 ... 105 247 104 127 206 min 208"
								newmin = 208
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127")):
								comment = "26: 2 42 10 ... 68 105 247 104 127 min 214"
								newmin = 214
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247")):
								comment = "24: 2 42 10 ... 243 174 68 105 247 min 207"
								newmin = 207
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105")):
								comment = "23: 2 42 10 ... 173 243 174 68 105 min 208"
								newmin = 208
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174")):
								comment = "21: 2 42 10 ... 52 173 243 174 min 208"
								newmin = 208
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243")):
								comment = "20: 2 42 10 ... 52 173 243 min 208"
								newmin = 208
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173")):
								comment = "19: 2 42 10 ... 44 27 4 52 173 min 208"
								newmin = 208
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52")):
								comment = "18: 2 42 10 ... 44 27 4 52 min 207"
								newmin = 207
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4")):
								comment = "17: 2 42 10 ... 44 27 4 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 29")):
								comment = "15: 2 42 10 ... 45 12 44 + 29 min 205"
								newmin = 205
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 32")):
								comment = "15: 2 42 10 ... 45 12 44 + 32 min 205"
								newmin = 205
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44")):
								comment = "15: 2 42 10 ... 45 12 44 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 46")):
								comment = "14: 2 42 10 ... 21 45 12 + 46 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 48")):
								comment = "14: 2 42 10 ... 21 45 12 + 48 min 205"
								newmin = 205
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12")):
								comment = "14: 2 42 10 ... 21 45 12 min 207"
								newmin = 207
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45")):
								comment = "13: 2 42 10 ... 59 21 45 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 46")):
								comment = "12: 2 42 10 ... 8 59 21 + 46 min 205"
								newmin = 205
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21")):
								comment = "12: 2 42 10 ... 8 59 21 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 59")):
								comment = "11: 2 42 10 ... 15 8 59 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 56")):
								comment = "10: 2 42 10 ... 20 15 8 + 56 min 205"
								newmin = 205
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8, 58")):
								comment = "10: 2 42 10 ... 20 15 8 + 58 min 205"
								newmin = 205
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15, 8")):
								comment = "10: 2 42 10 ... 20 15 8 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 15")):
								comment = "9: 2 42 10 43 24 6 20 15 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20, 21")):
								comment = "8: 2 42 10 43 24 6 20 + 21 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 20")):
								comment = "8: 2 42 10 43 24 6 20 min 207"
								newmin = 207
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6, 25")):
								comment = "7: 2 42 10 43 24 6 + 25 min 205"
								newmin = 205
							elif (fullmatch.startswith("[2, 42, 10, 43, 24, 6")):
								comment = "7: 2 42 10 43 24 6 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2, 42, 10, 43, 24")):
								comment = "6: 2 42 10 43 24 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2, 42, 10, 43, 21")):
								comment = "5: 2 42 10 43 + 21 min 205"
								newmin = 205
							elif (fullmatch.startswith("[2, 42, 10, 43")):
								comment = "5: 2 42 10 43 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2, 42, 10")):
								comment = "4: 2 42 10 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2, 42")):
								comment = "3: 2 42 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2")):
								comment = "2: 2 min 206"
								newmin = 206
							elif (fullmatch.startswith("[1, 28")):
								comment = "1: 1 28 min 204"
								newmin = 204
							elif (fullmatch.startswith("[1, 30")):
								comment = "1: 1 30 min 201"
								newmin = 201
							elif (fullmatch.startswith("[1, 27")):
								comment = "1: 1 27 min 204"
								newmin = 204
							elif (fullmatch.startswith("[3, 29")):
								comment = "1: 3 29 min 204"
								newmin = 204
							elif (fullmatch.startswith("[4, 25")):
								comment = "1: 4 25 min 204"
								newmin = 204
							elif (fullmatch.startswith("[4, 23")):
								comment = "1: 4 23 min 204"
								newmin = 204
							else:
								comment = "1: Non 2 min 205"
								newmin = 205
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

#QCleanup.rangeReader(0,62,211,True)
#QCleanup.reader(96,205,True)
#QCleanup.reader(56,1,True,"[2, 42, 10, 43, 24, 6, 20, 15, 8, 59, 21, 45, 12, 44, 27, 4, 52, 173, 243, 174, 68, 105, 247, 104, 127, 206, 151, 235, 244, 192, 81, 16, 18, 237, 249, 240, 77, 248, 203, 85, 119, 182, 138, 219, 226, 123, 239, 36, 31, 108, 165, 212, 210, 83, 84")
#QCleanup.reader(6,1,True,"[")
#QCleanup.table(180)
#QCleanup.viewer()
#QCleanup.cleanser(200, 6)
#QCleanup.viewCounter(550000)
#QCleanup.updateFrom96(217)
# True indicates using new minimum function which only shows iterations that need updating
QCleanup.runParser(550000,1,269,True,11000) 