from CreateTile import CreateTile
from EternityMCTS import EternityMCTS
from collections import Counter
import numpy as np
import time
import random
import json
import os.path

class EternityStart():
    def main():
        #random.seed(0)
        maxEpisodes = 1
        optionsCount = 0
        sampleSize = 3 #(1m is good - try several runs rather than 1 for comparison)
        CreateTile.firstCountLimit = 20000000 # will eventually be used for early iterations - keeping high for terminal solution (1m for test)
        episode = 1
        cutoff = 90 # Point at which we move from sample check to full solution
        Q = [] # Q list table with state and maximum amount for that state [1] and number of visits [2]
        currentVisitCount = 0
        terminalState = False # graceful way to end program where empty list
        file1 = open("MCTS.txt", "w") # detail for each episode (overwritten each time)
        file2 = open("MCTSRunSummary.txt", "a") # summary of tree and lookahead info
        if (os.path.isfile('Q-Table.txt') == True):
            with open("Q-table.txt", "r") as QTablefile:
                Q = json.load(QTablefile)
            print(f"Q-table uploaded with {len(Q)} lines")
        CreateTile.createTile()
        CreateTile.findPatternMatches()
        episodeList = [] # list of episode lengths
        maximaList = [] # list of maxima at each iteration 
        while episode <= maxEpisodes:
            start = time.time()
            MCTSList = []
            MCTSPosition = []
            newTilePositions = [] # Trying to positions within using original tileList
            testList = []
            testPosition = []
            averageList = []
            maxList = []
            epsilonMaxList = []
            maximaList = [] # depth of lookahead at each iteration - changed to iteration length
            a = []
            limitedRunList = []
            earlyList = []
            terminalState = False
            countLimit = CreateTile.firstCountLimit
            while (len(MCTSList) <= cutoff and terminalState == False):
                options = EternityMCTS.findNextPositionMatches(MCTSList,newTilePositions, True)
                optionsCount += len(options)
                if len(options) != len(set(options)):
                    print("There are DUPLICATE options to deal with that needs further testing\n")
                    file1.write("There are DUPLICATE options to deal with that needs further testing\n")
                    duplicate = True
                if (173 in options):
                    file1.write("ROTATION: This list contains tile 173 that may have two positions\n")
                if (199 in options):
                    file1.write("ROTATION: This list contains tile 199 that may have two positions\n")
                if (233 in options):
                    file1.write("ROTATION: This list contains tile 233 that may have two positions\n")
                random.shuffle(options)
                print(f"The new options would be {options} and the length is {len(options)} and cumulative {optionsCount}")
                file1.write(f"{options}\n")
                if (len(options) > 1 or 173 in options or 233 in options or 199 in options):
                    for item in Q:
                        if MCTSList == item[0]: 
                            #print(f"MCTS is {MCTSList} and item[0] is {item[0]}\n")
                            currentVisitCount = item[2] - 1 # Adjusting so epsilon is 1 unless previous sample taken
                    #if (currentVisitCount >= 1):
                    #    epsilon = 0.0
                    #else:
                    #    epsilon = 1.0
                    epsilon = 100/ (100 + currentVisitCount)		
                    print(f"Epsilon is set at {epsilon:.5f} and visitCount at {currentVisitCount}")
                    currentVisitCount = 0
			        #epsilon = 1 #test out completely random policy
                    # Three options - random, sample maximum or current largest maximum as tree policy
                    # In order to learn, using sample maximum and largest maximum for tree policy and avoiding random
                    if (random.random() < epsilon):
                        print(f"SAMPLE: Proceeding with sample testing and using results of sample")
                        sampleMax = True
                    else:
                        print(f"GREEDY: Taking the current largest maximum value without another sample test")
                        file1.write(f"GREEDY: Taking the current largest maximum value without another sample test\n")
                        sampleMax = False
                    for tile in options:
                        itemFound = False
                        testList.append(tile)
                        testPosition.append(CreateTile.tileList[tile].copy())
                        print(f"\nThe test list is {testList}")
                        # Implicitly does not deal with tiles that can have two positions
                        tilePositions = EternityMCTS.tileAlignment(testList)
                        #print(f"TEMP: The tile positions are {tilePositions}")
                        newTilePositions = EternityMCTS.tileAlignmentOnPositions(testList, testPosition)
                        #print(f"TEMP: The new tile positions are {newTilePositions}")
                        # 250 = 2m 250k likely a day
                        if (sampleMax == True):
                            for count in range(sampleSize):
                                # Now working with solution list so need length
                                limitedRunList = EternityMCTS.fullSolutionCheck(256, countLimit, testList.copy(), newTilePositions.copy())
                                if (len(limitedRunList) >= 200):                                    
                                    print(f"200+ solution reached of \n{limitedRunList}")
                                    file2.write(f"200+ solution reached of \n{limitedRunList}\n")
                                a.append(len(limitedRunList))
                                testList = MCTSList.copy()
                                testPosition = MCTSPosition.copy()
                                testList.append(tile)
                                testPosition.append(CreateTile.tileList[tile])
                            print("The distribution for runs is as follows:")
                            print(sorted(Counter(a).items())) # See if this works
                            #file1.write(f"{Counter(a)}\n")
                            average = sum(a)/len(a)
                            maximum = max(Counter(a))
                            print(f"The average is {average:.5f} and maximum was {maximum}")
                            # Extremely long section to deal with 173 and 233 edge cases of double rotation
                            # As these tiles are not rotated yet, it's taking default position which is misleading
                            # Need to force alignment first
                            if (tile == 173 or tile == 233 or tile == 199):
                                tilePositions = EternityMCTS.tileAlignment(testList)
                                newTilePositions = EternityMCTS.tileAlignmentOnPositions(testList, testPosition)
                                northMatch = testPosition[-1][0]
                                eastMatch = testPosition[-1][1]
                                southMatch = testPosition[-1][2]
                                westMatch = testPosition[-1][3]
                                print(f"Current tile is {tile} with position {testPosition[-1]}")
                                file1.write(f"Current tile is {tile} with position {testPosition[-1]}\n")
                                if (southMatch == westMatch):
                                    print("Second potential rotation needs to be tested\n")
                                    file1.write("Second potential rotation needs to be tested\n")
                                    # Rotation is clockwise
                                    if (southMatch == eastMatch):
                                        CreateTile.rotatePosition(-1, testPosition)
                                    else:
                                        CreateTile.rotatePosition(-1, testPosition)
                                        CreateTile.rotatePosition(-1, testPosition)
                                        CreateTile.rotatePosition(-1, testPosition)
                                    print(f"The new position is {testPosition[-1]}\n")
                                    file1.write(f"The new position is {testPosition[-1]}\n")
                                    b = []
                                    for count in range(sampleSize):
                                        limitedRunList = EternityMCTS.fullSolutionCheck(256, countLimit, testList.copy(), newTilePositions.copy())
                                        if (len(limitedRunList) >= 200):                                    
                                            print(f"200+ solution reached of \n{limitedRunList}")
                                            file2.write(f"200+ solution reached of \n{limitedRunList}")
                                        b.append(len(limitedRunList))
                                        testList = MCTSList.copy()
                                        testPosition = MCTSPosition.copy()
                                        testList.append(tile)
                                        testPosition.append(CreateTile.tileList[tile].copy())
                                    print("The distribution for the second run is as follows:")
                                    print(sorted(Counter(b).items())) # See if this works
                                    #file1.write(f"{Counter(b)}\n")
                                    average2 = sum(b)/len(b)
                                    maximum2 = max(Counter(b))
                                    print(f"The average is {average2:.5f} and maximum was {maximum2}")
                                    if (maximum2 > maximum):
                                        print(f"The second rotation was better and is being used")
                                        maximum = maximum2
                                        average = average2
                                    else:
                                        print(f"The first rotation was better or the same and is being used")
                                        maximum2 = maximum
                                        average2 = average
                                        eastMatch = testPosition[-1][1]
                                        southMatch = testPosition[-1][2]
                                        # better to use revised S and E here - less confusing
                                        if (southMatch == eastMatch):
                                            CreateTile.rotatePosition(-1, testPosition)
                                        else:
                                            CreateTile.rotatePosition(-1, testPosition)
                                            CreateTile.rotatePosition(-1, testPosition)
                                            CreateTile.rotatePosition(-1, testPosition)
                                    b = []
                                    northMatch = testPosition[-1][0]
                                    eastMatch = testPosition[-1][1]
                                    southMatch = testPosition[-1][2]
                                    westMatch = testPosition[-1][3]
                                    print(f"Final rotation used was {northMatch} {eastMatch} {southMatch} {westMatch}\n")
                                    file1.write(f"Final rotation used was {northMatch} {eastMatch} {southMatch} {westMatch}\n")
                                else:
                                    print("No further rotations need to be tested as W and S are different\n")
                            averageList.append(average)
                            maxList.append(maximum)
                            if len(Q) == 0:
                                Q.append([MCTSList.copy(),maximum,0])
                        # Should be done for greedy and non-greedy
                        for item in Q:  
                            #print(f"Item is {item}")
                            if testList == item[0]:
                                #print(f"item[0] is {item[0]}")
                                item[2] = item[2] + 1
                                if (sampleMax == True):
                                    item[1] = max(item[1],maximum)
                                epsilonMaxList.append(item[1])
                                itemFound = True
                                break;
                        if (itemFound == False):
                            #print(f"testlist {testList} is not in Q")
                            Q.append([testList.copy(), maximum, 1])
                            epsilonMaxList.append(maximum)
                        testList = MCTSList.copy()
                        testPosition = MCTSPosition.copy()
                        a.clear()
                        end = time.time()
                        print(f"Time taken so far is: {end - start:.3f} seconds")
                    print(f"\nFor options {options}")
                    # Choice of using average list or maximum list
                    if (sampleMax == True):
                        print(f"The averages were {averageList}, sample maxima were {maxList} and greedy maxima were {epsilonMaxList}")
                        file1.write(f"Average List:\n{averageList}\nSample Maxima:\n{maxList}\nGreedy Maxima:\n{epsilonMaxList}\n\n")
                    else:
                        print(f"GREEDY RUN: The greedy maxima were {epsilonMaxList}")
                        file1.write(f"GREEDY RUN: Greedy Maxima:\n{epsilonMaxList}\n\n")
                if (len(options) > 1 or maxList != []):                    
                    #maxOption = options[averageList.index(max(averageList))]
                    if (sampleMax == True):
                        maxOption = options[maxList.index(max(maxList))]
                        MCTSList.append(maxOption)
                        MCTSPosition.append(CreateTile.tileList[maxOption].copy())
                    else:
                        epsilonMaxOption = options[epsilonMaxList.index(max(epsilonMaxList))]
                        MCTSList.append(epsilonMaxOption)
                        MCTSPosition.append(CreateTile.tileList[epsilonMaxOption].copy())
                    testList = MCTSList.copy()
                    testPosition = MCTSPosition.copy()
                    #print(f"The maximum AVERAGE was {max(averageList)} so option {maxOption} was chosen and tree search is {MCTSList}\n")
                    if (sampleMax == True):
                        print(f"The maximum VALUE using SAMPLING was {max(maxList)} so option {maxOption} was chosen and tree search is {MCTSList}")
                        file1.write(f"\nThe maximum VALUE using SAMPLING was {max(maxList)} so option {maxOption} was chosen\n")    
                        # Propogate maxes up the tree (even from earlier iterations and also to single solutions)
                        earlyList = MCTSList.copy()
                        maxLength = max(maxList)
                        while(earlyList != []):
                            itemFound = False
                            for item in Q:                   
                                if earlyList == item[0]:
                                    if (item[1] < maxLength):
                                        print(f"{earlyList} has had its maximum updated to {maxLength} from {item[1]}")
                                    item[1] = max(item[1],maxLength)
                                    itemFound = True
                                    break
                            if (itemFound == False):
                                Q.append([earlyList.copy(), maxLength, 1])
                            earlyList.pop()
                    else:
                        print(f"The maximum VALUE using GREEDY MAX was {max(epsilonMaxList)} so option {epsilonMaxOption} was chosen and tree search is {MCTSList}")
                        file1.write(f"\nThe maximum VALUE using GREEDY MAX was {max(epsilonMaxList)} so option {epsilonMaxOption} was chosen\n")                    
                    print(f"The length of the tree search is {len(MCTSList)}\n")
                    file1.write(f"The length of the tree search is {len(MCTSList)}\n")
                    file1.write(f"{MCTSList}\n\n")
                    if (sampleMax == True):
                        maximaList.append(max(maxList)) # work out look ahead value
                    elif (maximaList != []):
                        maximaList.append(maximaList[-1])
                elif (len(options) == 1):
                    MCTSList.append(options[0])
                    MCTSPosition.append(CreateTile.tileList[options[0]].copy())
                    testList = MCTSList.copy()
                    testPosition = MCTSPosition.copy()
                    print(f"Only a single option {options[0]} so no random samples undertaken\n")
                    if (maximaList != []):
                        maximaList.append(maximaList[-1])
                elif (maxList == []):
                    terminalState = True
                    print(f"\nFinal tree length was {len(MCTSList)} which was \n{MCTSList}")
                    maxMCTS = MCTSList.copy() # just in case MCTS does not reach 88
                    file2.write(f"\nFinal tree length was {len(MCTSList)} which was \n{MCTSList}\n")
                    file1.write(f"\nFinal tree length was: {len(MCTSList)}\n")
                    finalLength = len(MCTSList)
                tilePositions = EternityMCTS.tileAlignment(testList)
                newTilePositions = EternityMCTS.tileAlignmentOnPositions(testList, testPosition)
                averageList.clear()
                maxList.clear()
                epsilonMaxList.clear()
            # New sense check - will become alternate full solution test after iteration 88 but not working atm
            verificationList = MCTSList.copy()
            verificationPositions = EternityMCTS.tileAlignmentOnPositions(testList, testPosition)
            if (len(verificationList) >= cutoff):
                cutoff = 256 # full solution test
                print (f"\nUndertaking full solution sense check with cutoff of {cutoff}\n") 
                countLimit = 5000000000
                maxMCTS = EternityMCTS.fullSolutionCheck(cutoff, countLimit, verificationList[:88], verificationPositions[:88])
                cutoff = 90# back to sample check for future episodes
                finalLength = len(maxMCTS)
                countLimit = CreateTile.firstCountLimit
                print("FINAL RESULTS")
                print(f"Length of final solution was {finalLength}\n")
                print(f"The solution was\n{maxMCTS}")
                file2.write(f"Final solution from {cutoff} iteration was of length {finalLength} and the solution itself was:\n{maxMCTS}\n")
            print(f"The length of the final Q-table with state, maximum, visitcount was {len(Q)}\n")
            print(f"The lookahead for each iteration for sample size {sampleSize} and count {countLimit} was {maximaList} and maximum was {max(maximaList)} with average {sum(maximaList)/len(maximaList):.3f}\n")
            file1.write(f"The lookahead for each iteration for sample size {sampleSize} and count {countLimit} was {maximaList} and maximum was {max(maximaList)} with average {sum(maximaList)/len(maximaList):.3f}\n")
            file1.write(f"Final Q-table length: {len(Q)}\n\n\n")
            file2.write(f"The lookahead for each iteration for sample size {sampleSize} and count {countLimit} was {maximaList} and maximum was {max(maximaList)} with average {sum(maximaList)/len(maximaList):.3f}\n")
            end = time.time()
            file2.write(f"Time taken for the complete run was: {end - start:.3f} seconds\n")
            file2.write(f"Final Q-table length: {len(Q)}\n\n")
            episodeList.append(len(maxMCTS)) 
            MCTSList = verificationList.copy()
            while(MCTSList != []):
                itemFound = False
                for item in Q:                   
                    if MCTSList == item[0]:
                        item[1] = max(item[1],finalLength)
                        itemFound = True
                # Should add to Q even for single options where no sampling was previously done (but not past cutoff)
                if (itemFound == False and len(MCTSList) <=cutoff):
                    Q.append([MCTSList.copy(), finalLength, 1])
                MCTSList.pop()
            print(f"The final length of {finalLength} has been used to update all prior Q table values\n")
            # Final update for original leaf
            Q[0][1] = max(Q[0][1],finalLength)
            Q[0][2] = Q[0][2] + 1
            with open("Q-table.txt","w") as handler:
                json.dump(Q,handler) 
            handler.close()             
            episode += 1    
            optionsCount = 0
        print(f"\nFor the {episode - 1} episodes run with sample size {sampleSize} and count {countLimit} the longest run was {max(episodeList)}")
        print(f"\nThe longest recorded run in the Q-Table is {Q[0][1]}")
        file1.close()

    main()



