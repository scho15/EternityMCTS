from CreateTile import CreateTile
import random

class EternityMCTS():

    # Input: usedTile list and whether corner hints should be used (True/False)
    # Output: list of matches with tile number only (not rotated)
    # [Assumes input list is in correct rotated position]
    def findNextPositionMatches(usedTiles, positions, useHints):

        consecutivePatterns = [] # List of tiles with two consecutive patterns
        tileSwap = False # When randomising double rotation tiles, the swap should only be made if 2 consecutive patterns have been used
        iteration = len(usedTiles) + 1

        if (iteration < 16):
            if (iteration == 1):
                consecutivePatterns = CreateTile.findConsecutivePatternMatches(0,0)
            else:
                consecutivePatterns = CreateTile.findConsecutivePatternMatches(0,positions[iteration-2][1])

        if (iteration == 16):
            #consecutivePatterns = CreateTile.findThreeConsecutivePatternMatches(0, 0, positions[iteration-2][1])
            #print(f"TEMP: Patterns with old consecutivePatterns are {consecutivePatterns}")
            consecutivePatterns = CreateTile.findThreeConsecutivePatternMatches(0, 0, positions[iteration-2][1])
            #print(f"TEMP: Patterns with new consecutivePatterns are {consecutivePatterns}")

        if (iteration > 16 and iteration%16 == 1):
            consecutivePatterns = CreateTile.findConsecutivePatternMatches(positions[iteration-17][0],0)

        if (iteration > 16 and iteration%16 != 0 and iteration%16 != 1):
            firstMatch = positions[iteration - 17][0]
            secondMatch = positions[iteration - 2][1]

            if (useHints == True):
                # Introducing constraints on hint on level lower. Arguable whether this is good for upper hint tiles
                if (iteration != 19 and iteration !=30 and iteration != 104 and iteration != 195 and iteration != 206):
                    consecutivePatterns = CreateTile.findConsecutivePatternMatches(firstMatch,secondMatch)
                    tileSwap = True
                elif (iteration == 19):
                    # ensuring iteration 19 has Northern tile of 15 as well as matching S and W
                    consecutivePatterns = CreateTile.findThreeConsecutivePatternMatches(firstMatch, secondMatch, 15)
                    #print(f"TEMP: Patterns with old consecutivePatterns are {consecutivePatterns}")
                    #consecutivePatterns = CreateTile.findAltThreeConsecutivePatternMatches(firstMatch, secondMatch, 15)
                    #print(f"TEMP: Patterns with old consecutivePatterns are {consecutivePatterns}")
                elif (iteration == 30):
                    # ensuring iteration 30 has Northern tile of 18 as well as matching S and W
                    consecutivePatterns = CreateTile.findThreeConsecutivePatternMatches(firstMatch, secondMatch, 18)
                elif (iteration == 104):
                    consecutivePatterns = CreateTile.findThreeConsecutivePatternMatches(firstMatch, secondMatch, 17)
                elif (iteration == 195):
                    consecutivePatterns = CreateTile.findThreeConsecutivePatternMatches(firstMatch, secondMatch, 10)
                elif (iteration == 206):
                    consecutivePatterns = CreateTile.findThreeConsecutivePatternMatches(firstMatch, secondMatch, 7)
            else:
                if (iteration == 104):
                    consecutivePatterns = CreateTile.findThreeConsecutivePatternMatches(firstMatch, secondMatch, 17)
                else:
                    consecutivePatterns = CreateTile.findConsecutivePatternMatches(firstMatch,secondMatch)
                    tileSwap = True

            # Adding hints for centre tile
            if (iteration == 120):
                if (firstMatch != 17) and (secondMatch != 10):
                    consecutivePatterns.clear()
                elif (139 not in consecutivePatterns):
                    consecutivePatterns.clear()
                if (139 in consecutivePatterns):
                    consecutivePatterns = [139]
            if (139 in consecutivePatterns and iteration != 120):
                consecutivePatterns.remove(139)

            if (useHints == True):
                # Hint for SW tile
                if (iteration == 35):
                    if (firstMatch != 15) and (secondMatch != 10):
                        consecutivePatterns.clear()
                    # Does not automatically ensure that 181 is selected
                    elif (181 not in consecutivePatterns):
                        consecutivePatterns.clear()
                    if (181 in consecutivePatterns):
                        consecutivePatterns = [181]
                if (181 in consecutivePatterns and iteration != 35):
                    consecutivePatterns.remove(181)
                # Hint for SE tile
                if (iteration == 46):
                    if (firstMatch != 18) and (secondMatch != 20):
                        consecutivePatterns.clear()
                    elif (249 not in consecutivePatterns):
                        consecutivePatterns.clear()
                    if (249 in consecutivePatterns):
                        consecutivePatterns = [249]
                if (249 in consecutivePatterns and iteration != 46):
                    consecutivePatterns.remove(249)
                # Hint for NW tile (partly academic!)
                if (iteration == 211):
                    if (firstMatch != 10) and (secondMatch != 13):
                        consecutivePatterns.clear()
                    elif (208 not in consecutivePatterns):
                        consecutivePatterns.clear()
                    if (208 in consecutivePatterns):
                        consecutivePatterns = [208]
                if (208 in consecutivePatterns and iteration != 211):
                    consecutivePatterns.remove(208)
                # Hint for NE tile (partly academic!)
                if (iteration == 222):
                    if (firstMatch != 7) and (secondMatch != 8):
                        consecutivePatterns.clear()
                    elif (255 not in consecutivePatterns):
                        consecutivePatterns.clear()
                    if (255 in consecutivePatterns):
                        consecutivePatterns = [255]
                if (255 in consecutivePatterns and iteration != 222):
                    consecutivePatterns.remove(255)

        if (iteration > 16 and iteration%16 == 0):
            firstMatch = positions[iteration - 17][0]
            #print(f'Edge to match on the South is {firstMatch}') # Optional Line 4
            secondMatch = positions[iteration - 2][1]
            #print(f'Edge to match on the West is {secondMatch}') # Optional Line 5
            thirdMatch = 0
            #print(f"Need to match outside edge {thirdMatch} as well") # Optional Line 6
            consecutivePatterns = CreateTile.findThreeConsecutivePatternMatches(0,firstMatch,secondMatch)

        # Remove items in usedTiles that have already been used
        for item in usedTiles:
            if item in consecutivePatterns[:]:
                consecutivePatterns.remove(item)
        # Remove items that are corner or edge tiles that won't fit
        for item in consecutivePatterns[:]:
            if (item <= 60 and iteration > 16 and iteration%16 != 0 and iteration%16 != 1):
                consecutivePatterns.remove(item)
            elif (item <=4 and iteration != 1 and iteration != 16 and iteration != 241 and iteration != 256):
                consecutivePatterns.remove(item)

        #
        # Logic issue - should only do swap where it's for 2 patterns not three
        #for item in consecutivePatterns[:]:
        #    if ((item == 173 or item == 199 or item == 233) and tileSwap == True):
        #        event = random.randint(0,1)
        #        westMatch = CreateTile.tileList[item][3]
        #        southMatch = CreateTile.tileList[item][2]
        #        if (westMatch == southMatch and event == 1):
        #            CreateTile.swapPosition(item)
        #            #print(f"{item} swap occurred using tileList (only position tileList kept)")
        tileSwap = False
        
        return consecutivePatterns

    # Input: usedTileList (list of integers)
    # Output: list of tiles in correct rotation assuming only last tile needs to be rotated
    def tileAlignmentOnLastPosition(usedList, positions):

        # Removal of for loop, taking all but last element and no other changes required
        tileList = positions.copy()[:-1]
        index = len(usedList) - 1
        iteration = index + 1 
        matchTile = usedList[-1]
            
        if (iteration < 16):
            if (iteration != 1):
                while (positions[index][2] != 0):
                    CreateTile.rotatePosition(index, positions)
                    #print(f"Rotation to ensure edges aligned so we have tile {matchTile} now at {positions[index]}")
            else:
                while (positions[index][2] != 0 or positions[index][3] != 0):
                    CreateTile.rotatePosition(index, positions)
        elif (iteration == 16):
            #print(f"\nConsidering the rotation of {matchTile} at iteration {iteration} which is currently {positions[index]}")
            while (positions[index][2] != 0 or positions[index][1] != 0):
                CreateTile.rotatePosition(index, positions)
                #print(f"Rotation to ensure corners aligned so we have tile {matchTile} now at {positions[index]}")

        if (iteration > 16 and iteration%16 == 1):
            while (positions[index][3] != 0):
                CreateTile.rotatePosition(index, positions)
                #print(f"Rotation to ensure edge aligned so we have tile {matchTile} now at {positions[index]}")
        elif (iteration > 16 and iteration%16 == 0):
            while (positions[index][1] != 0):
                CreateTile.rotatePosition(index, positions)
                #print(f"Rotation to ensure edge aligned so we have tile {matchTile} now at {positions[index]}")
        elif (iteration > 16):
            firstMatch = positions[iteration - 17][0]
            secondMatch = positions[iteration - 2][1]
            while (positions[index][2] != firstMatch or positions[index][3] != secondMatch):
                #print(f'Relevant match is at {positions[index][2]}')
                CreateTile.rotatePosition(index, positions)
                #print(f"Rotation to ensure tiles aligned so we have tile {matchTile} now at {positions[index]}") #Optional Line 10
        tileList.append(positions[index])

        return tileList


    #Main change to original version is using findNextPositionMatches rather than findNextMatches
    def fullSolutionCheck(cutoff,countLimit, inputSolution, positions, useHints):
    # Need 3 different elements - unexplored path, explored path and currentPath/usedtiles        
        
        exploredTiles = []
        unexploredTiles = []
        iteration = len(inputSolution) + 1
        minimumLength = len(inputSolution) 
        tempList = []
        count = 0
        maxIteration = 0
        maxMCTS = inputSolution
        doubleTile = 0 # Working out how many times 173,199 and 233 are used for testing
        SWMatch = 0 # Working out how many times double rotation tiles are used for testing
        termination = False # check to see if unexploredtiles are empty i.e. = [] at end
        oldPosition = []
        #Seeing if lengths can start from input solution
        #while (len(exploredTiles) <= iteration):
        #    exploredTiles.append([])
        #    unexploredTiles.append([])
        while (iteration <= cutoff and termination == False):
            # Next matches as a list
            if (unexploredTiles == [] and count != 0):
                termination = True
                break
            if (count > countLimit):
                termination = True
                break
            count += 1
            # Significantly simplified code to re-use findNextMatches and keep explored tiles check below
            consecutivePatterns = EternityMCTS.findNextPositionMatches(inputSolution, positions, useHints)
            
            if (exploredTiles != [] and len(exploredTiles[-1]) != 0):
                for item in exploredTiles[-1]:
                    if item in consecutivePatterns:
                        consecutivePatterns.remove(item)
                #print(f"Explored tiles for iteration is {exploredTiles[iteration-1]}")
            #print(f"Matching tiles list after explored tile purge is {consecutivePatterns}") # Optional Line 8
            # Take first eligible tile (for breadth first search would need to print them all out
            if (len(consecutivePatterns) != 0):
                # Migrating to random
                choice = random.randint(0,len(consecutivePatterns) - 1)
                matchTile = consecutivePatterns[choice]
                consecutivePatterns.pop(choice)
                if (unexploredTiles == [] or len(unexploredTiles) <= iteration - minimumLength - 1):
                    unexploredTiles.append(consecutivePatterns.copy()) # only place where unexploredTiles is appended apart from length
                    exploredTiles.append([])
                else:
                    unexploredTiles[-1] = consecutivePatterns.copy()
                # Adding to used tile list
                inputSolution.append(matchTile)
                positions.append(CreateTile.tileList[matchTile])
                positions = EternityMCTS.tileAlignmentOnLastPosition(inputSolution, positions)
                # Begin checking for adding or removal of double rotation tiles
                #if (matchTile == 173 or matchTile == 199 or matchTile == 233):
                #    doubleTile += 1
                #    print(f"Double rotation tile {matchTile} has just been added with position {positions[-1]} and count {doubleTile}")
                #    if (positions[-1][2] == positions[-1][3]):
                #        SWMatch += 1
                #        print(f"South and West tiles match so double rotation is possible with count {SWMatch}")
                #print(f"TEMP Line 274:Positions has been amended to {positions}")                              
                if (iteration > maxIteration):
                    maxIteration = iteration
                    if (maxIteration >= 190 and count > CreateTile.firstCountLimit or maxIteration >= 200):
                        print(f"Iteration is {iteration} and count is {count} with maximum iteration reached of {maxIteration}")
                        print(f"Latest solution is\n{inputSolution}")
                    maxCheck = True
                    maxMCTS = inputSolution.copy()
                iteration +=1
            elif (unexploredTiles != []):
                while (unexploredTiles!= [] and len(unexploredTiles[-1]) == 0):
                    # Begin checking for adding or removal of double rotation tiles
                    #if (inputSolution[-1] == 173 or inputSolution[-1] == 199 or inputSolution[-1] == 233):
                    #    doubleTile -= 1
                    #    print(f"Double rotation tile {inputSolution[-1]} has just been removed with position {positions[-1]} and count is now {doubleTile}")
                    #    if (positions[-1][2] == positions[-1][3]):
                    #        SWMatch -= 1
                    #        print(f"South and West tiles matched so double rotation was possible with count reduced to {SWMatch}")
                    inputSolution.pop()
                    unexploredTiles.pop()
                    positions.pop() # Newly added
                    exploredTiles.pop() # always reduces length by one - may also need to clear?
                    iteration -=1
                    #print(f'The last unexploredTile is now {unexploredTiles[-1]}') # Optional Line 14
                if (unexploredTiles!= [] and len(unexploredTiles[-1])!=0):
                    iteration -= 1
                    #print(f'The unexplored list is \n {unexploredTiles}') # Optional Line 15
                    #if (inputSolution[-1] == 173 or inputSolution[-1] == 199 or inputSolution[-1] == 233):
                    #    doubleTile -= 1
                    #    print(f"Double rotation tile {inputSolution[-1]} has just been removed with position {positions[-1]} and count is now {doubleTile}")
                    #    if (positions[-1][2] == positions[-1][3]):
                    #        SWMatch -= 1
                    #        print(f"South and West tiles matched so double rotation was possible with count reduced to {SWMatch}")
                    exploredTiles[-1].append(inputSolution.pop()) # Only place where explored is appended
                    positions.pop()
            # Originally add if iteration == maxIteration and maxCheck == True or (iteration <= 91 and count > 500000)
            if (count%250000000 == 0):
                print(f"\nUsed tiles list at count {count} is now \n{inputSolution}\n and iteration reached was {maxIteration}")
                print(f"Unexplored tiles at iteration {iteration} are \n{unexploredTiles}")
                print(f"Explored tiles at iteration {iteration} are \n{exploredTiles}")
                if (unexploredTiles != []):
                    for i, val in enumerate(unexploredTiles):
                        if (minimumLength + i <= minimumLength + 10 and len(inputSolution) > i+minimumLength):
                            print(f"{minimumLength+i+1}\t{inputSolution[i+minimumLength]} {val} {exploredTiles[i]}")                
                    maxCheck = False # Optional Insert Line 18 to get all iterations           
        return maxMCTS

    # Check to see if matching two or three tiles (to work out if double rotation swapping is a good thing
    def iterationCheck(iteration, useHints):
        tileSwap = False

        # Don't need to worry about edge tiles as 173 etc will not be considered

        if (useHints == True and iteration!= 19 and iteration != 30 and iteration != 104 and iteration != 195 and iteration != 206):
            tileSwap = True

        if (useHints == False and iteration!= 104):
            tileSwap = True

        return tileSwap

    #Main change to original version is using findNextPositionMatches rather than findNextMatches
    def fullSolutionCheckWithSwap(cutoff,countLimit, inputSolution, positions, useHints):
    # Need 3 different elements - unexplored path, explored path and currentPath/usedtiles        
        
        exploredTiles = []
        unexploredTiles = []
        iteration = len(inputSolution) + 1
        minimumLength = len(inputSolution) 
        tempList = []
        count = 0
        maxIteration = 0
        swapCheck = False # Verify if double rotation may be an issue (for 2 rather than 3 consecutive matches)
        maxMCTS = inputSolution
        doubleTile = 0 # Working out how many times 173,199 and 233 are used for testing
        SWMatch = [False,False,False] # Check to see if match 177,199,233 are in tree
        termination = False # check to see if unexploredtiles are empty i.e. = [] at end
        alternativeMatch = [False,False,False] # See if alternative position has been tried
        special = False #Catch all log to see if alternative matches have been triggered
        #Seeing if lengths can start from input solution
        #while (len(exploredTiles) <= iteration):
        #    exploredTiles.append([])
        #    unexploredTiles.append([])
        while (iteration <= cutoff and termination == False):
            special = False # reset flag for each iteration - not sure this is the right position
            # Next matches as a list
            if (unexploredTiles == [] and count != 0):
                termination = True
                break
            if (count > countLimit):
                termination = True
                break
            count += 1
            # Significantly simplified code to re-use findNextMatches and keep explored tiles check below
            consecutivePatterns = EternityMCTS.findNextPositionMatches(inputSolution, positions, useHints)
            
            if (exploredTiles != [] and len(exploredTiles[-1]) != 0):
                for item in exploredTiles[-1]:
                    if item in consecutivePatterns:
                        consecutivePatterns.remove(item)
                #print(f"Explored tiles for iteration is {exploredTiles[iteration-1]}")
            #print(f"Matching tiles list after explored tile purge is {consecutivePatterns}") # Optional Line 8
            # Take first eligible tile (for breadth first search would need to print them all out
            if (len(consecutivePatterns) != 0):
                # Migrating to random
                choice = random.randint(0,len(consecutivePatterns) - 1)
                matchTile = consecutivePatterns[choice]
                consecutivePatterns.pop(choice)
                if (unexploredTiles == [] or len(unexploredTiles) <= iteration - minimumLength - 1):
                    unexploredTiles.append(consecutivePatterns.copy()) # only place where unexploredTiles is appended apart from length
                    exploredTiles.append([])
                else:
                    unexploredTiles[-1] = consecutivePatterns.copy()
                # Adding to used tile list
                inputSolution.append(matchTile)
                positions.append(CreateTile.tileList[matchTile])
                positions = EternityMCTS.tileAlignmentOnLastPosition(inputSolution, positions)
                # Begin checking for adding or removal of double rotation tiles
                if ((matchTile == 173 or matchTile == 199 or matchTile == 233) and (positions[-1][2] == positions[-1][3])):    
                    if (inputSolution[-1] == 173):
                        SWMatch[0] = True
                    elif(inputSolution[-1] == 199):
                        SWMatch[1] = True
                    elif(inputSolution[-1] == 233):
                        SWMatch[2] = True
                    #print(f"Double rotation tile {matchTile} has just been added with position   {positions[-1]} and SWcount is {SWMatch} on iteration {iteration} and count {count}")
                #print(f"TEMP Line 274:Positions has been amended to {positions}")                              
                if (iteration > maxIteration):
                    maxIteration = iteration
                    if (maxIteration >= 190 and count > CreateTile.firstCountLimit or maxIteration >= 200):
                        print(f"Iteration is {iteration} and count is {count} with maximum iteration reached of {maxIteration}")
                        print(f"Latest solution is\n{inputSolution}")
                    maxCheck = True
                    maxMCTS = inputSolution.copy()
                iteration +=1
            elif (unexploredTiles != []):
                while (unexploredTiles!= [] and len(unexploredTiles[-1]) == 0):
                    # Begin checking for adding or removal of double rotation tiles
                    if ((inputSolution[-1] == 173 or inputSolution[-1] == 199 or inputSolution[-1] == 233) and (positions[-1][2] == positions[-1][3])):
                        swapCheck = EternityMCTS.iterationCheck(len(inputSolution), useHints) # changed to length of inputSolution
                        if (swapCheck == False):
                            print(f"TEST: Edge case found on iteration {len(inputSolution)} count {count} and tile {inputSolution[-1]} where swapping is not appropriate")
                        if (inputSolution[-1] == 173 and swapCheck == True):                            
                            # Check alternative for that match
                            if alternativeMatch[0] == False:
                                alternativeMatch[0] = True
                                special = True #Undertake a double rotation rather than pop inputSolution
                                oldPosition = positions[-1].copy()
                                positions[-1][0] = oldPosition[1]
                                positions[-1][1] = oldPosition[0]
                                #print(f"Position of tile {inputSolution[-1]} has been swapped from {oldPosition} to {positions[-1]} on iteration {iteration} and count {count}")
                            else:
                                special = False
                                alternativeMatch[0] = False
                                SWMatch[0] = False
                        elif(inputSolution[-1] == 199 and swapCheck == True):
                            if alternativeMatch[1] == False:
                                alternativeMatch[1] = True
                                special = True #Undertake a double rotation rather than pop inputSolution
                                oldPosition = positions[-1].copy()
                                positions[-1][0] = oldPosition[1]
                                positions[-1][1] = oldPosition[0]
                                #print(f"Position of tile {inputSolution[-1]} has been swapped from {oldPosition} to {positions[-1]} on iteration {iteration} and count {count}")
                            else:
                                special = False
                                alternativeMatch[1] = False
                                SWMatch[1] = False
                        elif(inputSolution[-1] == 233 and swapCheck == True):
                            if alternativeMatch[2] == False:
                                alternativeMatch[2] = True
                                special = True #Undertake a double rotation rather than pop inputSolution
                                oldPosition = positions[-1].copy()
                                positions[-1][0] = oldPosition[1]
                                positions[-1][1] = oldPosition[0]
                                #print(f"Position of tile {inputSolution[-1]} has been swapped from {oldPosition} to {positions[-1]} on iteration {iteration} and count {count}")
                            else:
                                special = False
                                alternativeMatch[2] = False
                                SWMatch[2] = False
                        else:
                            special = False
                        #if special == False:
                            #print(f"Double rotation tile {inputSolution[-1]} has just been removed with position {positions[-1]} and SWcount is {SWMatch}") 
                    if special == False:
                        inputSolution.pop()
                        unexploredTiles.pop()
                        positions.pop() # Newly added
                        exploredTiles.pop() # always reduces length by one - may also need to clear?
                        iteration -=1
                        #print(f'The last unexploredTile is now {unexploredTiles[-1]}') # Optional Line 14
                if (unexploredTiles!= [] and len(unexploredTiles[-1])!=0):
                    #print(f'The unexplored list is \n {unexploredTiles}') # Optional Line 15
                    # Begin checking for adding or removal of double rotation tiles
                    if ((inputSolution[-1] == 173 or inputSolution[-1] == 199 or inputSolution[-1] == 233) and (positions[-1][2] == positions[-1][3])):
                        swapCheck = EternityMCTS.iterationCheck(len(inputSolution), useHints) # RChanged to length of inputSolution
                        if (swapCheck == False):
                            print(f"TEST: Edge case found on iteration {len(inputSolution)} count {count} and tile {inputSolution[-1]} where swapping is not appropriate")
                        if (inputSolution[-1] == 173 and swapCheck == True):                            
                            # Check alternative for that match
                            if alternativeMatch[0] == False:
                                alternativeMatch[0] = True
                                special = True #Undertake a double rotation rather than pop inputSolution
                                oldPosition = positions[-1].copy()
                                positions[-1][0] = oldPosition[1]
                                positions[-1][1] = oldPosition[0]
                                #print(f"Position of tile {inputSolution[-1]} has been swapped from {oldPosition} to {positions[-1]} on iteration {iteration} and count {count}")
                            else:
                                special = False
                                alternativeMatch[0] = False
                                SWMatch[0] = False
                        elif(inputSolution[-1] == 199 and swapCheck == True):
                            if alternativeMatch[1] == False:
                                alternativeMatch[1] = True
                                special = True #Undertake a double rotation rather than pop inputSolution
                                oldPosition = positions[-1].copy()
                                positions[-1][0] = oldPosition[1]
                                positions[-1][1] = oldPosition[0]
                                #print(f"Position of tile {inputSolution[-1]} has been swapped from {oldPosition} to {positions[-1]} on iteration {iteration} and count {count}")
                            else:
                                special = False
                                alternativeMatch[1] = False
                                SWMatch[1] = False
                        elif(inputSolution[-1] == 233 and swapCheck == True):
                            if alternativeMatch[2] == False:
                                alternativeMatch[2] = True
                                special = True #Undertake a double rotation rather than pop inputSolution
                                oldPosition = positions[-1].copy()
                                positions[-1][0] = oldPosition[1]
                                positions[-1][1] = oldPosition[0]
                                #print(f"Position of tile {inputSolution[-1]} has been swapped from {oldPosition} to {positions[-1]} on iteration {iteration} and count {count}")
                            else:
                                special = False
                                alternativeMatch[2] = False
                                SWMatch[2] = False
                        else:
                            special = False # dealing with swapCheck = False
                        #if special == False:
                        #    print(f"Double rotation tile {inputSolution[-1]} has just been removed with position {positions[-1]} and SWcount is {SWMatch}") 
                    if special == False:
                        iteration -= 1
                        exploredTiles[-1].append(inputSolution.pop()) # Only place where explored is appended
                        positions.pop()
            # Originally add if iteration == maxIteration and maxCheck == True or (iteration <= 91 and count > 500000)
            if (count%250000000 == 0):
                print(f"\nUsed tiles list at count {count} is now \n{inputSolution}\n and iteration reached was {maxIteration}")
                print(f"Unexplored tiles at iteration {iteration} are \n{unexploredTiles}")
                print(f"Explored tiles at iteration {iteration} are \n{exploredTiles}")
                if (unexploredTiles != []):
                    for i, val in enumerate(unexploredTiles):
                        if (minimumLength + i <= minimumLength + 10 and len(inputSolution) > i+minimumLength):
                            print(f"{minimumLength+i+1}\t{inputSolution[i+minimumLength]} {val} {exploredTiles[i]}")                
                    maxCheck = False # Optional Insert Line 18 to get all iterations           
        return [maxMCTS,count-1]