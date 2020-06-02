import time
import random
import CreateTile

class EternityMCTS:

    def startMatching(cutoff):
        start = time.time()
        # Need 3 different elements - unexplored path, explored path and currentPath/usedtiles        

        iteration = 1
        exploredTiles.append([])
        count = 0
        maxIteration = 0

        while (iteration <= cutoff):
            # Next matches as a list
            count += 1
            if (iteration <= 16):
                if (iteration == 1):
                    consecutivePatterns = findConsecutivePatternMatches(0,0)
                else:
                    consecutivePatterns = findConsecutivePatternMatches(0,tileList[usedTiles[iteration-2]][1])
                # Temporary - to avoid getting stuck on iteration 34 for first choice model
                #if ((iteration == 6) and (16 in consecutivePatterns)):
                #    consecutivePatterns.remove(16)
                #    print(F"Temporary: Tile 16 has been removed at iteration 6 to avoid getting stuck")
            if (iteration == 16):
                consecutivePatterns = findThreeConsecutivePatternMatches(0, 0, tileList[usedTiles[iteration-2]][1])
                #print(f"Matching tile list at corner is {consecutivePatterns}") # Optional Line 1
            if (iteration > 16 and iteration%16 == 1):
                consecutivePatterns = findConsecutivePatternMatches(tileList[usedTiles[iteration-17]][0],0)
            if (iteration > 16 and iteration%16 != 0 and iteration%16 != 1):
                firstMatch = tileList[usedTiles[iteration - 17]][0]
                #print(f'Edge to match on the South is {firstMatch}') # Optional Line 2
                secondMatch = tileList[usedTiles[iteration - 2]][1]
                #print(f'Edge to match on the West is {secondMatch}') # Optional Line 3
                # Introducing constraints on hint on level lower. Arguable whether this is good for upper hint tiles
                if (iteration != 19 and iteration !=30 and iteration != 104 and iteration != 195 and iteration != 206):
                    consecutivePatterns = findConsecutivePatternMatches(firstMatch,secondMatch)
                elif (iteration == 19):
                    # ensuring iteration 19 has Northern tile of 15 as well as matching S and W
                    consecutivePatterns = findThreeConsecutivePatternMatches(firstMatch, secondMatch, 15)
                elif (iteration == 30):
                    # ensuring iteration 30 has Northern tile of 18 as well as matching S and W
                    consecutivePatterns = findThreeConsecutivePatternMatches(firstMatch, secondMatch, 18)
                elif (iteration == 104):
                    consecutivePatterns = findThreeConsecutivePatternMatches(firstMatch, secondMatch, 17)
                elif (iteration == 195):
                    consecutivePatterns = findThreeConsecutivePatternMatches(firstMatch, secondMatch, 10)
                elif (iteration == 206):
                    consecutivePatterns = findThreeConsecutivePatternMatches(firstMatch, secondMatch, 7)
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
                firstMatch = tileList[usedTiles[iteration - 17]][0]
                #print(f'Edge to match on the South is {firstMatch}') # Optional Line 4
                secondMatch = tileList[usedTiles[iteration - 2]][1]
                #print(f'Edge to match on the West is {secondMatch}') # Optional Line 5
                thirdMatch = 0
                #print(f"Need to match outside edge {thirdMatch} as well") # Optional Line 6
                consecutivePatterns = findThreeConsecutivePatternMatches(0,firstMatch,secondMatch)
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
            #print(f"Matching tiles list after used tile purge is {consecutivePatterns}") # Optional Line 7
            if (len(exploredTiles) <= iteration - 1):
                exploredTiles.append([])
            #print(f"exploredTiles is\n {exploredTiles}")
            #if (len(exploredTiles[iteration-1]) == 0): - changed else below to if and negated expression
            #    print(f"Explored tiles for iteration {iteration} are nil so can be ignored")
            if (len(exploredTiles[iteration-1]) != 0):
                for item in exploredTiles[iteration-1]:
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
                unexploredTiles.append(consecutivePatterns.copy())
                matchConfiguration = tileList[matchTile]
                #print(f"Selecting tile {matchTile} which currently has NESW configuration of {matchConfiguration}") # Optional Line 9
                # Rotate tile to ensure edges are correctly aligned - originally screwed up as used AND rather than OR below
                if (iteration < 16):
                    if (iteration != 1):
                        while (tileList[matchTile][2] != 0):
                            rotateTile(matchTile)
                            #print(f"Rotation to ensure edges aligned so we have tile {matchTile} now at {tileList[matchTile]}")
                    else:
                        while (tileList[matchTile][2] != 0 or tileList[matchTile][3] != 0):
                            rotateTile(matchTile)
                if (iteration == 16):
                    #print(f"\nConsidering the rotation of {matchTile} at iteration {iteration} which is currently {tileList[matchTile]}")
                    while (tileList[matchTile][2] != 0 or tileList[matchTile][1] != 0):
                        rotateTile(matchTile)
                        #print(f"Rotation to ensure corners aligned so we have tile {matchTile} now at {tileList[matchTile]}")
                if (iteration > 16 and iteration%16 == 1):
                    while (tileList[matchTile][3] != 0):
                        rotateTile(matchTile)
                        #print(f"Rotation to ensure edge aligned so we have tile {matchTile} now at {tileList[matchTile]}")
                elif (iteration > 16 and iteration%16 == 0):
                    while (tileList[matchTile][1] != 0):
                        rotateTile(matchTile)
                        #print(f"Rotation to ensure edge aligned so we have tile {matchTile} now at {tileList[matchTile]}")
                # 31.5.20: Changed 1 to 3 below which is a big change
                elif (iteration > 16):
                    while (tileList[matchTile][2] != firstMatch or tileList[matchTile][3] != secondMatch):
                        #print(f'Relevant match is at {tileList[matchTile][2]}')
                        rotateTile(matchTile)
                        #print(f"Rotation to ensure tiles aligned so we have tile {matchTile} now at {tileList[matchTile]}") #Optional Line 10
                # Adding to used tile list
                usedTiles.append(matchTile)
                if (iteration > maxIteration):
                    maxIteration = iteration
                    print(f"\nIteration is {iteration} and count is {count} with maximum iteration reached of {maxIteration}")
                    maxCheck = True
                iteration +=1
            else:
                #print(f'Attempting backtracking!') # Optional Line 11
                #print(f"Length of last unexplored tiles is {len(unexploredTiles[-1])}") # Optional Line 12
                # First go back and remove the last used tile that led to no solution
                # attempting while rather than if
                while (len(unexploredTiles[-1]) == 0):
                    #print(f'Removing the last iteration that was empty') # Optional Line 13
                    usedTiles.pop()
                    unexploredTiles.pop()
                    exploredTiles.pop() # always reduces length by one - may also need to clear?
                    exploredTiles[-1].clear() # yes results looking much better!!
                    iteration -=1
                    #print(f'The last unexploredTile is now {unexploredTiles[-1]}') # Optional Line 14
                if (len(unexploredTiles[-1])!=0):
                    iteration -=1
                    #print(f'The unexplored list is \n {unexploredTiles}') # Optional Line 15
                    # iteration - 1 is right given the zero start for exploredTiles
                    exploredTiles[iteration-1].append(usedTiles.pop()) # Only place where explored is appended
                    #print(f'Last entry on used tile list popped and added to explored category:\n  {usedTiles}\n{exploredTiles}') #Opt Line 16
                    #Consec tiles is re-determined for each level. Question whether to bypass this and use unexplored tiles instead
                    #consecutivePatterns.extend(unexploredTiles[-1]) - deleted as consec re-determined at start of loop
                    #print(f"Replacing empty option with unexplored options {consecutivePatterns}") # Optional Line 17
                    unexploredTiles.pop() 
            end = time.time()
            if ((iteration == maxIteration and maxCheck == True) or count%25000000 == 0):
                print(f"\nUsed tiles list at count {count} is now \n{usedTiles}\n and iteration reached was {maxIteration}")
                print(f"Unexplored tiles at iteration {iteration} are \n{unexploredTiles}")
                print(f"Explored tiles at iteration {iteration} are \n{exploredTiles}")
                for i, val in enumerate(unexploredTiles):
                    if i >= 75 and i <= 100:
                        print(f"{i+1}\t{usedTiles[i]} {val} {exploredTiles[i]}")
                print(f"Time taken in seconds was {end - start:.3f}")
                maxCheck = False # Optional Insert Line 18 to get all iterations
        end = time.time()
    
        print("FINAL RESULTS")
        print(f"Used tiles list is now \n{usedTiles}")
        print(f"Unexplored tiles at iteration {iteration - 1} are \n{unexploredTiles}")
        print(f"Explored tiles at iteration {iteration - 1} are \n{exploredTiles}")
        print(f"Time taken in seconds was {end - start:.3f}\n")


    def eternityStart():
        # Input iteration at which cutoff should occur
        cut = 220
        createTile()
        findPatternMatches()
        startMatching(cut)

eternityStart()
