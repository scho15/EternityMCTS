import json
import os.path
from collections import Counter

class QCleanup:
	# Simple file to read Q and see if any entries exceed 88 (and Q can be "dumped" back in edited form)
	# Could use later to sort through Q and see some interesting properties
	def cleanser(cutoff, minimumIteration, zero):
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
				if zero == True:
					item[2] = 0 # Only used for 203 or 205 reset
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

	def truncateToBestSoln(trunc,soln):
		Q = []
		a = []	
		b = []
		c = []
		cutoff = 0
		kept = 0
		remove = 0
		file = 'C:/Users/scho1/QTableMCTS/Run 1/QTableCombined.txt'
		# same as viewer although may want to specify file location
		if (os.path.isfile(file) == True):
			with open(file, "r") as QTablefile:
				Q = json.load(QTablefile)
				print(f"Q-table uploaded with {len(Q)} lines")
		for item in Q:
			length = len(item[0])
			a.append(length)
			b.append(item[1])
			c.append(item[2])
		print(f"Maximum and average iterations are {max(a)} and {sum(a)/len(a):.5f}")
		print(sorted(Counter(a).items()))
		a.clear()
		print(f"Maximum and average lengths are {max(b)} and {sum(b)/len(b):.5f}")
		print(sorted(Counter(b).items()))
		b.clear()
		print(f"Maximum and average visit count values are {max(c)} and {sum(c)/len(c):.5f}")
		print(sorted(Counter(b).items()))
		c.clear()
		# new operation
		print(f"\nFinding iterations that are {trunc} away from best solution so far")
		print(f"The following match the solution:\n{soln}")
		for item in Q.copy():
			if len(item[0]) - trunc <= 0:
				#print(f"{item[0]} cutoff")
				cutoff += 1
			elif (item[0][0:(len(item[0])-trunc)] == soln[0:(len(item[0])-trunc)] and len(item[0]) <= 96):
				#print(f"{item[0]} kept")
				kept += 1
			else:
				Q.remove(item)
				remove += 1
				if (remove%10000 == 0):
					print(f"{remove} items have been removed and items kept is {kept+cutoff}")
		print(f"Those below cutoff were {cutoff} and those above threshold were {kept}")

		for item in Q:
			length = len(item[0])
			a.append(length)
			b.append(item[1])
		print(f"Revised maximum and average are {max(a)} and {sum(a)/len(a):.5f} and length is {len(Q)}\n")
		print(sorted(Counter(a).items()))
		print(f"Revised maximum and average lengths are {max(b)} and {sum(b)/len(b):.5f}")
		print(sorted(Counter(b).items()))
		with open("C:/Users/scho1/QTableMCTS/QTable-Trunc.txt","w") as handler:
			json.dump(Q,handler) 
		handler.close()    

	def truncateFile(trunc, file):
		Q = [] # uploaded Q Table
		run = 0 # number of runs
		best = [] # list of best entries at 96
		highest = 0 # length of highest solution
		#trunc = 1 # finding solutions trunc away from best
		cutoff = 0 # entries of length below trunc
		kept = 0 # items kept in truncated table
		unused = 0 # items not used in table
		#iteration = 1 # count of iteration
		TruncQ = [] # truncated table with required solutions

		# Upload Q Table
		if (os.path.isfile(file) == True):
			with open(file, "r") as QTablefile:
				Q = json.load(QTablefile)
				print(f"Q Table uploaded with {len(Q)} lines")
		# Determine highest length at 96
		for item in Q:
			length = len(item[0])
			if (length == 96 and item[1] >= highest):					
				highest = item[1]
			if (length == 0):
				run = item[2]
		print(f"Runs recorded is (should be zero): {run}")
		# Determine entries with this highest length
		for item in Q:
			length = len(item[0])
			if (length == 96 and item[1] == highest):	
				best.append(item[0])
		print(f"Highest entries so far has length {highest} and are as follows:")
		for entry in best:
			print(entry)
		# Finding truncated solutions
		for entry in best:
			print(f"\nFinding iterations that are {trunc} away from best solutions so far:")
			print(entry)
			for item in Q.copy():
				if len(item[0]) - trunc <= 0:
					#print(f"{item[0]} cutoff")
					if item not in TruncQ:
						TruncQ.append(item)
						cutoff += 1
				elif (item[0][0:(len(item[0])-trunc)] == entry[0:(len(item[0])-trunc)] and len(item[0]) <= 96):
					#print(f"{item[0]} kept")
					if item not in TruncQ:
						TruncQ.append(item)
						kept += 1
				else:
					unused += 1
					if (unused%50000 == 0):
						print(f"{unused} items have been removed and items kept is {kept+cutoff}")
			print(f"Those below cutoff were {cutoff} and those above threshold were {kept}")
			print(f"Truncated table has {len(TruncQ)} entries from all best solutions so far")
			unused = 0
		with open("C:/Users/scho1//QTableMCTS/QSeeded.txt","w") as handler:
			json.dump(TruncQ,handler) 
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

	def qCombine(location1, location2):
		identical = 0
		different = 0
		found = False
		Q1 = []
		Q2 = []
		#location1 = 'C:/Users/scho1/QTableMCTS/Run 1/QTableCombined.txt'
		#location2 = 'C:/Users/scho1/QTableMCTS/QTable.txt'
		Q1 = QCleanup.qTableViewer(location1)
		Q2 = QCleanup.qTableViewer(location2)
		for item2 in Q2.copy():
			for item1 in Q1.copy():
				if (item1[0] == item2[0]):
					identical += 1
					found = True
					#print(f"{item1[0]} appears in both tables with maxes {item1[1]} and {item2[1]}")
					item1[1] = max(item1[1],item2[1])
			if (found == False):
				different += 1	
				Q1.append(item2)
				if (different%10000 == 0):
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
		with open("C:/Users/scho1/QTableMCTS/QTableNEWCombined.txt","w") as handler:
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
		lt190count = 0 # counting items less than 190 in final
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
							if (fullmatch.startswith("[1")):
								comment = "2: 1 min 209"
								newmin = 209
							elif (fullmatch.startswith("[3")):
								comment = "Non 1: 3 min 206"
								newmin = 206
							elif (fullmatch.startswith("[2")):
								comment = "Non 1: 2 min 206"
								newmin = 206
							elif (fullmatch.startswith("[4")):
								comment = "Non 1: 4 min 206"
								newmin = 206
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
							if compact[4] < 190:
								lt190count += 1
							# May need tuning for higher iterations - set at 1 hr at present
							if (size == 300000):
								timing = 750
							elif (size == 350000):
								timing = 800
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
			print(f"The counter of final values for {size} had an average of {sum(cnt2.elements())/sum(cnt2.values()):.2f} for {sum(cnt2.values())} runs with {lt190count} less than 190 and was:\n {sorted(cnt2.items())}")
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

	def lowest(num):
		Q = []
		lowest = 256
		output = ""
		QDictLength = {}
		QDictVisits = {}
		if (os.path.isfile('C:/Users/scho1/QTableMCTS/QTable.txt') == True):
			with open("C:/Users/scho1/QTableMCTS/QTable.txt", "r") as QTablefile:
				Q = json.load(QTablefile)
				print(f"Q Table uploaded with {len(Q)} lines")
		print(f"Lowest entries for iterations 1 to 6:")
		for iteration in range(1,7):
			for item in Q:
				length = len(item[0])
				if (length == iteration and item[1] < lowest):					
					lowest = item[1]
			output += str(lowest) + " "
			lowest = 256
		print (output)
		output = ""
		for iteration in range(1,7):
			for item in Q:
				length = len(item[0])
				if (length == iteration and item[1] < lowest and item[0][0] == num):					
					lowest = item[1]
					#print(item[0])
			output += str(lowest) + " "
			lowest = 256
		print (output)

	def progress():
		Q = [] # uploaded Q Table
		OldTruncQ = [] # uploaded truncated table
		run = 0 # number of runs
		TruncQ = [] # truncated table with required solutions
		best = [] # list of best entries at 96
		bestItn = 0 # best iteration so far from 1 - 4
		count = 0 # counting through solutions
		highest = 0 # length of highest solution
		trunc = 1 # finding solutions trunc away from best
		cutoff = 0 # entries of length below trunc
		kept = 0 # items kept in truncated table
		unused = 0 # items not used in table
		a = [] # list of lengths
		identical = 0 # used when comparing tables 
		different = 0 # used when comparing tables
		addition = 0 # used when comparing tables
		found = False # used when comparing tables
		# Upload Q Table
		if (os.path.isfile('C:/Users/scho1/QTableMCTS/QTable.txt') == True):
			with open("C:/Users/scho1/QTableMCTS/QTable.txt", "r") as QTablefile:
				Q = json.load(QTablefile)
				print(f"Q Table uploaded with {len(Q)} lines")
		if (os.path.isfile('C:/Users/scho1/QTableMCTS/QTruncated.txt') == True):
			with open("C:/Users/scho1/QTableMCTS/QTruncated.txt", "r") as QTruncatedfile:
				OldTruncQ = json.load(QTruncatedfile)
				print(f"Old truncated Q Table uploaded with {len(OldTruncQ)} lines")
		# Determine highest length at 96
		for item in Q:
			length = len(item[0])
			if (length == 96 and item[1] >= highest):					
				highest = item[1]
			if (length == 0):
				run = item[2]
		print(f"Number of runs so far is: {run}")
		# Determine entries with this highest length
		for item in Q:
			length = len(item[0])
			if (length == 96 and item[1] == highest):	
				best.append(item[0])
		print(f"Highest entries so far has length {highest} and are as follows:")
		for entry in best:
			print(entry)
		# Finding truncated solutions
		for entry in best:
			print(f"\nFinding iterations that are {trunc} away from best solutions so far:")
			print(entry)
			for item in Q.copy():
				if len(item[0]) == 2 and item[0][0] != best[count][0]:
					#print(f"{item[0]} cutoff")
					cutoff += 1
					if item not in TruncQ:
						TruncQ.append(item)
				elif (item[0][0:len(item[0])-trunc] == entry[0:len(item[0])-trunc] and len(item[0]) <= 96):
					#print(f"{item[0]} kept")
					kept += 1
					if item not in TruncQ:
						TruncQ.append(item)
				else:
					unused += 1
			bestItn = best[count][0]
			print(f"Non {bestItn} Iterations: {cutoff}\t{bestItn} Iterations: {kept}\tUnused: {unused}")
			print(f"Truncated table has {len(TruncQ)} entries from all best solutions so far")
			for item in TruncQ:
				if len(item[0]) == 2 and item[0][0] == 1:
					a.append(item[1])
			print(f"1 iteration: {sorted(Counter(a).items())}")
			a.clear()
			for item in TruncQ:
				if len(item[0]) == 2 and item[0][0] == 2:
					a.append(item[1])
			print(f"2 iteration: {sorted(Counter(a).items())}")
			a.clear()
			for item in TruncQ:
				if len(item[0]) == 2 and item[0][0] == 3:
					a.append(item[1])
			print(f"3 iteration: {sorted(Counter(a).items())}")
			a.clear()
			for item in TruncQ:
				if len(item[0]) == 2 and item[0][0] == 4:
					a.append(item[1])
			print(f"4 iteration: {sorted(Counter(a).items())}")
			a.clear()
			for item in TruncQ:
				if len(item[0]) <= 1:
					a.append(item[1])
			print(f"First Element 1 2 3 4: {sorted(Counter(a).items())}")
			QCleanup.counting(a)
			a.clear()
			for item in TruncQ:
				if item[0][0] == best[count][0] and len(item[0]) <= 16 and item[0][0:len(item[0])-trunc] == entry[0:len(item[0])-trunc]:
					a.append(item[1])
			print(f"{best[count][0]} iterations:")
			print(f"1 - 16: {sorted(Counter(a).items())}")
			QCleanup.counting(a)
			a.clear()
			for item in TruncQ:
				if item[0][0] == best[count][0] and len(item[0]) >= 17 and len(item[0]) <= 32 and item[0][0:len(item[0])-trunc] == entry[0:len(item[0])-trunc]:
					a.append(item[1])
			print(f"17 - 32: {sorted(Counter(a).items())}")
			QCleanup.counting(a)
			a.clear()
			for item in TruncQ:
				if item[0][0] == best[count][0] and len(item[0]) >= 33 and len(item[0]) <= 48 and item[0][0:len(item[0])-trunc] == entry[0:len(item[0])-trunc]:
					a.append(item[1])
			print(f"33 - 48: {sorted(Counter(a).items())}")
			QCleanup.counting(a)
			a.clear()
			for item in TruncQ:
				if item[0][0] == best[count][0] and len(item[0]) >= 49 and len(item[0]) <= 64 and item[0][0:len(item[0])-trunc] == entry[0:len(item[0])-trunc]:
					a.append(item[1])
			print(f"49 - 64: {sorted(Counter(a).items())}")
			QCleanup.counting(a)
			a.clear()
			for item in TruncQ:
				if item[0][0] == best[count][0] and len(item[0]) >= 65 and len(item[0]) <= 80 and item[0][0:len(item[0])-trunc] == entry[0:len(item[0])-trunc]:
					a.append(item[1])
			print(f"65 - 80: {sorted(Counter(a).items())}")
			QCleanup.counting(a)
			a.clear()
			for item in TruncQ:
				if item[0][0] == best[count][0] and len(item[0]) >= 81 and len(item[0]) <= 96 and item[0][0:len(item[0])-trunc] == entry[0:len(item[0])-trunc]:
					a.append(item[1])
			print(f"81 - 96: {sorted(Counter(a).items())}")
			QCleanup.counting(a)
			a.clear()
			for item in TruncQ:
				if (item[0][0] == best[count][0] and len(item[0]) <= 96 and item[0][0:len(item[0])-trunc] == entry[0:len(item[0])-trunc]) or (len(item[0]) == 1 and item[0][0] != best[0][0]):
					a.append(item[1])
			print(f"{best[0][0]} iterations totals:\n{sorted(Counter(a).items())}")
			QCleanup.counting(a)
			a.clear()
			cutoff = 0 # entries of length below trunc
			kept = 0 # items kept in truncated table
			unused = 0 # items not used in table
			count += 1
		with open("C:/Users/scho1//QTableMCTS/QTruncated.txt","w") as handler:
			json.dump(TruncQ,handler) 
		handler.close()   
		# Comparing to previous version of truncated file
		for item2 in TruncQ.copy():
			for item1 in OldTruncQ.copy():
				if (item1[0] == item2[0]):
					found = True
					#print(f"{item1[0]} appears in both tables with maxes {item1[1]} and {item2[1]}")
					if (item1[1] == item2[1]):
						identical += 1
					else:
						different += 1
						print(f"{item1[0]} went from {item1[1]} to {item2[1]}")
			if (found == False):
				addition += 1
				print(f"{item2[0]} with length {item2[1]} is a new addition")
			found = False
		print(f"The truncated tables had {identical} matches, {different} updates and {addition} new additions")

	def progressByIteration():
		Q = [] # uploaded Q Table
		run = 0 # number of runs
		best = [] # list of best entries at 96
		highest = 0 # length of highest solution
		trunc = 1 # finding solutions trunc away from best
		cutoff = 0 # entries of length below trunc
		kept = 0 # items kept in truncated table
		unused = 0 # items not used in table
		iteration = 1 # count of iteration
		TruncQ = [] # truncated table with required solutions
		a = [] # list of lengths
		# seeded with other non-best iteration
		b = [207, 207, 207] # cumulative list of lengths

		# Upload Q Table
		if (os.path.isfile('C:/Users/scho1/QTableMCTS/QTable.txt') == True):
			with open("C:/Users/scho1/QTableMCTS/QTable.txt", "r") as QTablefile:
				Q = json.load(QTablefile)
				print(f"Q Table uploaded with {len(Q)} lines")
		# Determine highest length at 96
		for item in Q:
			length = len(item[0])
			if (length == 96 and item[1] >= highest):					
				highest = item[1]
			if (length == 0):
				run = item[2]
		print(f"Number of runs so far is: {run}")
		# Determine entries with this highest length
		for item in Q:
			length = len(item[0])
			if (length == 96 and item[1] == highest):	
				best.append(item[0])
		print(f"Highest entries so far has length {highest} and are as follows:")
		for entry in best:
			print(entry)
		# Finding truncated solutions
		for entry in best:
			print(f"\nFinding iterations that are {trunc} away from best solutions so far:")
			print(entry)
			for item in Q.copy():
				if len(item[0]) == 2 and item[0][0] != entry[0]:
					#print(f"{item[0]} cutoff")
					cutoff += 1
					if item not in TruncQ:
						TruncQ.append(item)
				elif (item[0][0:len(item[0])-trunc] == entry[0:len(item[0])-trunc] and len(item[0]) <= 96):
					#print(f"{item[0]} kept")
					kept += 1
					if item not in TruncQ:
						TruncQ.append(item)
				else:
					unused += 1
			print(f"Non {entry[0]} Iterations: {cutoff}\t{entry[0]} Iterations: {kept}\tUnused: {unused}")
			print(f"Truncated table has {len(TruncQ)} entries from all best solutions so far")

			while iteration <= 96:
				for item in TruncQ:
					if item[0][0] == entry[0] and len(item[0]) == iteration and item[0][0:len(item[0])-trunc] == entry[0:len(item[0])-trunc]:
						a.append(item[1])
						b.append(item[1])
				print(f"{iteration}: {sorted(Counter(a).items())}")
				a.clear()
				if iteration%16 == 0:
					QCleanup.counting(b)
				iteration += 1				
			for item in TruncQ:
				if (item[0][0] == entry[0] and len(item[0]) <= 96 and item[0][0:len(item[0])-trunc] == entry[0:len(item[0])-trunc]) or (len(item[0]) == 1 and item[0][0] != entry[0]):
					a.append(item[1])
			print(f"{entry[0]} iterations totals:\n{sorted(Counter(a).items())}")
			QCleanup.counting(a)
			a.clear() 
			b = [207, 207, 207]
			cutoff = 0 # entries of length below trunc
			kept = 0 # items kept in truncated table
			unused = 0 # items not used in table
			iteration = 1

	def counting(a):
		sum205 = 0
		sum204 = 0
		sum203 = 0
		sum202 = 0
		nonvbl = 0
		b = a.copy()
		for elt in b:
			if elt >= 205:
				sum205 += 1
			elif elt == 204:
				sum204 += 1
			elif elt == 203:
				sum203 += 1
			elif elt >= 185:
				sum202 += 1
			else:
				nonvbl += 1
		print(f"205+: {sum205}\t\t204: {sum204}\t\t203: {sum203}\t\t202-: {sum202}\t\t Non Viable: {nonvbl}\t\tTotal: {sum205+sum204+sum203+sum202+nonvbl}")
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
		sum190 = 0 # entries 190 and over
		sum200 = 0 # entries 200 and over
		sum205 = 0 # entries 205 and over
		total = 0 # total of all entries
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
		storedList = storedCntr.items()
		for a, b in storedList:
			a = int(a)
			#print(f"First element is {a}")
			total += b
			if (a >= 190):
				sum190 += b
			if (a >= 200):
				sum200 += b
			if (a >= 205):
				sum205 += b
		print(f"200+: {sum200} \t{sum200*100/total:.4f}%\t\t190+: {sum190} \t{sum190*100/total:.4f}%\t205+: {sum205} \t{sum205*100/total:.4f}%")

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

#Used during runs
#QCleanup.reader(96,211,True)
#QCleanup.viewer()
#QCleanup.table(190)
#QCleanup.lowest(1)
#QCleanup.viewCounter(750000)
#QCleanup.rangeReader(0,97,211,True)
#QCleanup.runParser(2000000,1,60,True,0) 
#QCleanup.reader(4,1,True, "[1")
#QCleanup.progress()
QCleanup.progressByIteration()
# Used end of every run - true for final cleansing
#QCleanup.cleanser(203, 6, False)
# Used every 4 runs 
#QCleanup.qCombine('C:/Users/scho1/QTableMCTS/Run 8/QTableFINALRun8.txt','C:/Users/scho1/QTableMCTS/QTable5-7Combined.txt') # Used very rarely!
#QCleanup.truncateFile(6, 'C:/Users/scho1/QTableMCTS/QTable5-8Combined.txt')
# Viewing tables other than current one
#QCleanup.qTableViewer("C:/Users/scho1/QTableMCTS/Run 1/QTableFINALRun1.txt")
#QCleanup.reader(3,1,True,"[","C:/Users/scho1/QTableMCTS/Run A/QTableFINALRunA.txt")