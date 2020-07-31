from CreateTile import CreateTile
import random

class EternityMCTS():

    # Input: usedTile list and whether corner hints should be used (True/False)
    # Output: list of matches with tile number only (not rotated)
    # [Assumes input list is in correct rotated position]
    def findNextMatches(usedTiles, useHints):

        consecutivePatterns = [] # List of tiles with two consecutive patterns

        iteration = len(usedTiles) + 1

        if (iteration <= 16):
            if (iteration == 1):
                consecutivePatterns = CreateTile.findConsecutivePatternMatches(0,0)
            else:
                consecutivePatterns = CreateTile.findConsecutivePatternMatches(0,CreateTile.tileList[usedTiles[iteration-2]][1])

        if (iteration == 16):
            consecutivePatterns = CreateTile.findThreeConsecutivePatternMatches(0, 0, CreateTile.tileList[usedTiles[iteration-2]][1])

        if (iteration > 16 and iteration%16 == 1):
            consecutivePatterns = CreateTile.findConsecutivePatternMatches(CreateTile.tileList[usedTiles[iteration-17]][0],0)

        if (iteration > 16 and iteration%16 != 0 and iteration%16 != 1):
            firstMatch = CreateTile.tileList[usedTiles[iteration - 17]][0]
            secondMatch = CreateTile.tileList[usedTiles[iteration - 2]][1]

            if (useHints == True):
                # Introducing constraints on hint on level lower. Arguable whether this is good for upper hint tiles
                if (iteration != 19 and iteration !=30 and iteration != 104 and iteration != 195 and iteration != 206):
                    consecutivePatterns = CreateTile.findConsecutivePatternMatches(firstMatch,secondMatch)
                elif (iteration == 19):
                    # ensuring iteration 19 has Northern tile of 15 as well as matching S and W
                    consecutivePatterns = CreateTile.findThreeConsecutivePatternMatches(firstMatch, secondMatch, 15)
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
            firstMatch = CreateTile.tileList[usedTiles[iteration - 17]][0]
            #print(f'Edge to match on the South is {firstMatch}') # Optional Line 4
            secondMatch = CreateTile.tileList[usedTiles[iteration - 2]][1]
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

        for item in consecutivePatterns[:]:
            if (item == 173 or item == 199 or item == 233):
                event = random.randint(0,1)
                westMatch = CreateTile.tileList[item][3]
                southMatch = CreateTile.tileList[item][2]
                if (westMatch == southMatch and event == 1):
                    CreateTile.swapPosition(item)
                    #print(f"{item} swap occurred")

        return consecutivePatterns

        # Input: usedTile list and whether corner hints should be used (True/False)
    # Output: list of matches with tile number only (not rotated)
    # [Assumes input list is in correct rotated position]
    def findNextPositionMatches(usedTiles, positions, useHints):

        consecutivePatterns = [] # List of tiles with two consecutive patterns

        iteration = len(usedTiles) + 1

        if (iteration <= 16):
            if (iteration == 1):
                consecutivePatterns = CreateTile.findConsecutivePatternMatches(0,0)
            else:
                consecutivePatterns = CreateTile.findConsecutivePatternMatches(0,positions[iteration-2][1])

        if (iteration == 16):
            consecutivePatterns = CreateTile.findThreeConsecutivePatternMatches(0, 0, positions[iteration-2][1])

        if (iteration > 16 and iteration%16 == 1):
            consecutivePatterns = CreateTile.findConsecutivePatternMatches(positions[iteration-17][0],0)

        if (iteration > 16 and iteration%16 != 0 and iteration%16 != 1):
            firstMatch = positions[iteration - 17][0]
            secondMatch = positions[iteration - 2][1]

            if (useHints == True):
                # Introducing constraints on hint on level lower. Arguable whether this is good for upper hint tiles
                if (iteration != 19 and iteration !=30 and iteration != 104 and iteration != 195 and iteration != 206):
                    consecutivePatterns = CreateTile.findConsecutivePatternMatches(firstMatch,secondMatch)
                elif (iteration == 19):
                    # ensuring iteration 19 has Northern tile of 15 as well as matching S and W
                    consecutivePatterns = CreateTile.findThreeConsecutivePatternMatches(firstMatch, secondMatch, 15)
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

        # Keep swap in for time being
        for item in consecutivePatterns[:]:
            if (item == 173 or item == 199 or item == 233):
                event = random.randint(0,1)
                westMatch = CreateTile.tileList[item][3]
                southMatch = CreateTile.tileList[item][2]
                if (westMatch == southMatch and event == 1):
                    CreateTile.swapPosition(item)
                    print(f"{item} swap occurred using tileList (only position tileList kept)")

        return consecutivePatterns

    # Input: usedTileList (list of integers)
    # Output: list of tiles in correct rotation
    def tileAlignment(usedList):
        tileList = [] 

        for index, matchTile in enumerate(usedList):

            iteration = index + 1 
            
            if (iteration < 16):
                if (iteration != 1):
                    while (CreateTile.tileList[matchTile][2] != 0):
                        CreateTile.rotateTile(matchTile)
                        #print(f"Rotation to ensure edges aligned so we have tile {matchTile} now at {CreateTile.tileList[matchTile]}")
                else:
                    while (CreateTile.tileList[matchTile][2] != 0 or CreateTile.tileList[matchTile][3] != 0):
                        CreateTile.rotateTile(matchTile)
            if (iteration == 16):
                #print(f"\nConsidering the rotation of {matchTile} at iteration {iteration} which is currently {CreateTile.tileList[matchTile]}")
                while (CreateTile.tileList[matchTile][2] != 0 or CreateTile.tileList[matchTile][1] != 0):
                    CreateTile.rotateTile(matchTile)
                    #print(f"Rotation to ensure corners aligned so we have tile {matchTile} now at {CreateTile.tileList[matchTile]}")
            if (iteration > 16 and iteration%16 == 1):
                while (CreateTile.tileList[matchTile][3] != 0):
                    CreateTile.rotateTile(matchTile)
                    #print(f"Rotation to ensure edge aligned so we have tile {matchTile} now at {CreateTile.tileList[matchTile]}")
            elif (iteration > 16 and iteration%16 == 0):
                while (CreateTile.tileList[matchTile][1] != 0):
                    CreateTile.rotateTile(matchTile)
                    #print(f"Rotation to ensure edge aligned so we have tile {matchTile} now at {CreateTile.tileList[matchTile]}")
            elif (iteration > 16):
                firstMatch = CreateTile.tileList[usedList[iteration - 17]][0]
                secondMatch = CreateTile.tileList[usedList[iteration - 2]][1]
                while (CreateTile.tileList[matchTile][2] != firstMatch or CreateTile.tileList[matchTile][3] != secondMatch):
                    #print(f'Relevant match is at {CreateTile.tileList[matchTile][2]}')
                    CreateTile.rotateTile(matchTile)
                    #print(f"Rotation to ensure tiles aligned so we have tile {matchTile} now at {CreateTile.tileList[matchTile]}") #Optional Line 10
            tileList.append(CreateTile.tileList[matchTile])

        return tileList

    # Input: usedTileList (list of integers)
    # Output: list of tiles in correct rotation
    def tileAlignmentOnPositions(usedList, positions):
        tileList = [] 

        for index, matchTile in enumerate(usedList):

            iteration = index + 1 
            
            if (iteration < 16):
                if (iteration != 1):
                    while (positions[index][2] != 0):
                        CreateTile.rotatePosition(index, positions)
                        #print(f"Rotation to ensure edges aligned so we have tile {matchTile} now at {positions[index]}")
                else:
                    while (positions[index][2] != 0 or positions[index][3] != 0):
                        CreateTile.rotatePosition(index, positions)
            if (iteration == 16):
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
    
    def startMatching(usedTiles):

        iteration = len (usedTiles) + 1 
        consecutivePatterns = EternityMCTS.findNextMatches(usedTiles,True)

        while (len(consecutivePatterns) != 0):
            # Migrating to random
            choice = random.randint(0,len(consecutivePatterns) - 1)
            matchTile = consecutivePatterns[choice]
            consecutivePatterns.pop(choice)
            matchConfiguration = CreateTile.tileList[matchTile]
            # Rotate tile to ensure edges are correctly aligned 
            if (iteration < 16):
                if (iteration != 1):
                    while (CreateTile.tileList[matchTile][2] != 0):
                        CreateTile.rotateTile(matchTile)
                        #print(f"Rotation to ensure edges aligned so we have tile {matchTile} now at {CreateTile.tileList[matchTile]}")
                else:
                    while (CreateTile.tileList[matchTile][2] != 0 or CreateTile.tileList[matchTile][3] != 0):
                        CreateTile.rotateTile(matchTile)
            if (iteration == 16):
                #print(f"\nConsidering the rotation of {matchTile} at iteration {iteration} which is currently {CreateTile.tileList[matchTile]}")
                while (CreateTile.tileList[matchTile][2] != 0 or CreateTile.tileList[matchTile][1] != 0):
                    CreateTile.rotateTile(matchTile)
                    #print(f"Rotation to ensure corners aligned so we have tile {matchTile} now at {CreateTile.tileList[matchTile]}")
            if (iteration > 16 and iteration%16 == 1):
                while (CreateTile.tileList[matchTile][3] != 0):
                    CreateTile.rotateTile(matchTile)
                    #print(f"Rotation to ensure edge aligned so we have tile {matchTile} now at {CreateTile.tileList[matchTile]}")
            elif (iteration > 16 and iteration%16 == 0):
                while (CreateTile.tileList[matchTile][1] != 0):
                    CreateTile.rotateTile(matchTile)
                    #print(f"Rotation to ensure edge aligned so we have tile {matchTile} now at {CreateTile.tileList[matchTile]}")
            # 31.5.20: Changed 1 to 3 below which is a big change
            elif (iteration > 16):
                firstMatch = CreateTile.tileList[usedTiles[iteration - 17]][0]
                secondMatch = CreateTile.tileList[usedTiles[iteration - 2]][1]
                while (CreateTile.tileList[matchTile][2] != firstMatch or CreateTile.tileList[matchTile][3] != secondMatch):
                    #print(f'Relevant match is at {CreateTile.tileList[matchTile][2]}')
                    CreateTile.rotateTile(matchTile)
                    #print(f"Rotation to ensure tiles aligned so we have tile {matchTile} now at {CreateTile.tileList[matchTile]}") #Optional Line 10
            # Adding to used tile list
            usedTiles.append(matchTile)           
            iteration += 1
            consecutivePatterns = EternityMCTS.findNextMatches(usedTiles,True)

        run = iteration - 1
        if (run >= 200):
            print(f"The length of the run is exceptional at {run}")
            print(f"usedTiles is at {usedTiles}")

        return run

    def fullSolutionCheck(cutoff,countLimit, inputSolution, positions):
    # Need 3 different elements - unexplored path, explored path and currentPath/usedtiles        
        
        exploredTiles = []
        unexploredTiles = []
        iteration = len(inputSolution) + 1
        minimumLength = len(inputSolution) 
        count = 0
        maxIteration = 0
        maxMCTS = inputSolution
        termination = False # check to see if unexploredtiles are empty i.e. = [] at end
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
            consecutivePatterns = EternityMCTS.findNextMatches(inputSolution, True)
            
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
                matchConfiguration = CreateTile.tileList[matchTile]
                #print(f"Selecting tile {matchTile} which currently has NESW configuration of {matchConfiguration}") # Optional Line 9
                # Rotate tile to ensure edges are correctly aligned - originally screwed up as used AND rather than OR below
                if (iteration < 16):
                    if (iteration != 1):
                        while (CreateTile.tileList[matchTile][2] != 0):
                            CreateTile.rotateTile(matchTile)
                            #print(f"Rotation to ensure edges aligned so we have tile {matchTile} now at {CreateTile.tileList[matchTile]}")
                    else:
                        while (CreateTile.tileList[matchTile][2] != 0 or CreateTile.tileList[matchTile][3] != 0):
                            CreateTile.rotateTile(matchTile)
                if (iteration == 16):
                    #print(f"\nConsidering the rotation of {matchTile} at iteration {iteration} which is currently {CreateTile.tileList[matchTile]}")
                    while (CreateTile.tileList[matchTile][2] != 0 or CreateTile.tileList[matchTile][1] != 0):
                        CreateTile.rotateTile(matchTile)
                        #print(f"Rotation to ensure corners aligned so we have tile {matchTile} now at {CreateTile.tileList[matchTile]}")
                if (iteration > 16 and iteration%16 == 1):
                    while (CreateTile.tileList[matchTile][3] != 0):
                        CreateTile.rotateTile(matchTile)
                        #print(f"Rotation to ensure edge aligned so we have tile {matchTile} now at {CreateTile.tileList[matchTile]}")
                elif (iteration > 16 and iteration%16 == 0):
                    while (CreateTile.tileList[matchTile][1] != 0):
                        CreateTile.rotateTile(matchTile)
                        #print(f"Rotation to ensure edge aligned so we have tile {matchTile} now at {CreateTile.tileList[matchTile]}")
                # 31.5.20: Changed 1 to 3 below which is a big change
                elif (iteration > 16):
                    firstMatch = CreateTile.tileList[inputSolution[iteration - 17]][0]
                    secondMatch = CreateTile.tileList[inputSolution[iteration - 2]][1]
                    while (CreateTile.tileList[matchTile][2] != firstMatch or CreateTile.tileList[matchTile][3] != secondMatch):
                        #print(f'Relevant match is at {CreateTile.tileList[matchTile][2]}')
                        CreateTile.rotateTile(matchTile)
                        #print(f"Rotation to ensure tiles aligned so we have tile {matchTile} now at {CreateTile.tileList[matchTile]}") #Optional Line 10
                # Adding to used tile list
                inputSolution.append(matchTile)
                # Checking for double rotation
                #if (matchTile == 173 and CreateTile.tileList[matchTile][2] == CreateTile.tileList[matchTile][3]):
                #    matchConfiguration = CreateTile.tileList[matchTile]
                #    print(f"matchTile {matchTile} is in tree in position {matchConfiguration} at count {count}")
                #elif (matchTile == 199 and CreateTile.tileList[matchTile][2] == CreateTile.tileList[matchTile][3]):
                #    matchConfiguration = CreateTile.tileList[matchTile]
                #    print(f"matchTile {matchTile} is in tree in position {matchConfiguration} at count {count}")
                #elif (matchTile == 233 and CreateTile.tileList[matchTile][2] == CreateTile.tileList[matchTile][3]):
                #    matchConfiguration = CreateTile.tileList[matchTile]
                #    print(f"matchTile {matchTile} is in tree in position {matchConfiguration} at count {count}")
                if (iteration > maxIteration):
                    maxIteration = iteration
                    if (maxIteration >= 190 and count > CreateTile.firstCountLimit or maxIteration >= 200):
                        print(f"Iteration is {iteration} and count is {count} with maximum iteration reached of {maxIteration}")
                        print(f"Latest solution is\n{inputSolution}")
                    maxCheck = True
                    maxMCTS = inputSolution.copy()
                iteration +=1
            elif (unexploredTiles != []):
                #print(f'Attempting backtracking!') # Optional Line 11
                #print(f"Length of last unexplored tiles is {len(unexploredTiles[-1])}") # Optional Line 12
                # First go back and remove the last used tile that led to no solution
                # attempting while rather than if
                while (unexploredTiles!= [] and len(unexploredTiles[-1]) == 0):
                    #print(f'Removing the last iteration that was empty') # Optional Line 13
                    #if (inputSolution[-1] == 173 and CreateTile.tileList[inputSolution[-1]][2] == CreateTile.tileList[inputSolution[-1]][3]):
                    #    CreateTile.doubleRotation[0] = True
                    #    matchConfiguration = CreateTile.tileList[inputSolution[-1]]
                    #    print(f"matchTile {inputSolution[-1]} is out of tree in position {matchConfiguration} at count {count}")
                    #elif (inputSolution[-1] == 199 and CreateTile.tileList[inputSolution[-1]][2] == CreateTile.tileList[inputSolution[-1]][3]):
                    #    CreateTile.doubleRotation[1] = True
                    #    matchConfiguration = CreateTile.tileList[inputSolution[-1]]
                    #    print(f"matchTile {inputSolution[-1]} is out of tree in position {matchConfiguration} at count {count}")
                    #elif (inputSolution[-1] == 233 and CreateTile.tileList[inputSolution[-1]][2] == CreateTile.tileList[inputSolution[-1]][3]):
                    #    CreateTile.doubleRotation[2] = True
                    #    matchConfiguration = CreateTile.tileList[inputSolution[-1]]
                    #    print(f"matchTile {inputSolution[-1]} is out of tree in position {matchConfiguration} at count {count}")
                    inputSolution.pop()
                    unexploredTiles.pop()
                    exploredTiles.pop() # always reduces length by one - may also need to clear?
                    #exploredTiles[-1].clear() # yes results looking much better!!
                    iteration -=1
                    #print(f'The last unexploredTile is now {unexploredTiles[-1]}') # Optional Line 14
                if (unexploredTiles!= [] and len(unexploredTiles[-1])!=0):
                    iteration -= 1
                    #print(f'The unexplored list is \n {unexploredTiles}') # Optional Line 15
                    # iteration - 1 is right given the zero start for exploredTiles
                    #if (inputSolution[-1] == 173 and CreateTile.tileList[inputSolution[-1]][2] == CreateTile.tileList[inputSolution[-1]][3]):
                    #    CreateTile.doubleRotation[0] = True
                    #    matchConfiguration = CreateTile.tileList[inputSolution[-1]]
                    #    print(f"matchTile {inputSolution[-1]} is out of tree in position {matchConfiguration} at count {count}")
                    #elif (inputSolution[-1] == 199 and CreateTile.tileList[inputSolution[-1]][2] == CreateTile.tileList[inputSolution[-1]][3]):
                    #    CreateTile.doubleRotation[1] = True
                    #    matchConfiguration = CreateTile.tileList[inputSolution[-1]]
                    #    print(f"matchTile {inputSolution[-1]} is out of tree in position {matchConfiguration} at count {count}")
                    #elif (inputSolution[-1] == 233 and CreateTile.tileList[inputSolution[-1]][2] == CreateTile.tileList[inputSolution[-1]][3]):
                    #    CreateTile.doubleRotation[2] = True
                    #    matchConfiguration = CreateTile.tileList[inputSolution[-1]]
                    #    print(f"matchTile {inputSolution[-1]} is out of tree in position {matchConfiguration} at count {count}")
                    exploredTiles[-1].append(inputSolution.pop()) # Only place where explored is appended
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