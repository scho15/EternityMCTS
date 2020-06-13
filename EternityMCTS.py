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