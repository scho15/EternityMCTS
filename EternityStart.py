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
        # DECISIONS REQUIRED
        useHints = True # Use only centre tile or 4 corner hints as well
        maxEpisodes = 7 # number of episodes to run
        sampleSize = 5 # number of runs/samples to take - at least 2 is recommended
        CreateTile.firstCountLimit = 2000000 # cutoff for run - normally at least 1m
        cutoff = 88 # Point at which we move from sample check to full solution
        # VARIABLES INITIALISATION
        #random.seed(1)
        optionsCount = 0
        episode = 1
        Q = [] # Q list table with state and maximum amount for that state [1] and number of visits [2]
        currentVisitCount = 0
        terminalState = False # graceful way to end program where empty list
        episodeList = [] # list of episode lengths
        maximaList = [] # list of maxima at each iteration 
        # FILE OPENING AND SETTING UP TILE AND PATTERN SETS
        file1 = open("MCTS.txt", "w") # detail for each episode (overwritten each time)
        file2 = open("MCTSRunSummary.txt", "a") # summary of tree and lookahead info
        if (os.path.isfile('Q-Table.txt') == True):
            with open("Q-table.txt", "r") as QTablefile:
                Q = json.load(QTablefile)
            print(f"Q-table uploaded with {len(Q)} lines")
        CreateTile.createTile()
        CreateTile.findPatternMatches() 
        CreateTile.findThreePatternMatches()
        # MAIN BODY FOR EACH EPISODE
        while episode <= maxEpisodes:
            start = time.time()
            MCTSList = []
            MCTSPosition = [] # Trying to use MCTS only
            testList = []
            #testPosition = [] # What worries me a little is whether double rotation gets overwritten if only testPosition is aligned
            averageList = []
            maxList = []
            epsilonMaxList = []
            maximaList = [] # depth of lookahead at each iteration - changed to iteration length
            a = [] # storing lengths of maximum iteration
            runLength = [] # storing count length
            limitedRunList = []
            earlyList = []
            runCount = 0
            terminalState = False
            countLimit = CreateTile.firstCountLimit
            while (len(MCTSList) <= cutoff and terminalState == False):
                options = EternityMCTS.findNextPositionMatches(MCTSList,MCTSPosition, useHints)
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
                    #epsilon = 0
                    #if (currentVisitCount >= 1):
                    #    epsilon = 0.0
                    #else:
                    #    epsilon = 1.0
                    epsilon = 100/ (100 + currentVisitCount)		
                    print(f"Epsilon is set at {epsilon:.5f} and visitCount at {currentVisitCount}")
                    currentVisitCount = 0
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
                        MCTSPosition.append(CreateTile.tileList[tile].copy())
                        MCTSPosition = EternityMCTS.tileAlignmentOnLastPosition(testList, MCTSPosition)
                        print(f"\nThe test list is {testList}")
                        # Implicitly does not deal with tiles that can have two positions - ideally stop using this
                        #tilePositions = EternityMCTS.tileAlignment(testList)
                        # print(f"TEMP: The tile positions are {tilePositions} using rotations to CreateTile tiles")                        
                        #print(f"TEMP: The new tile positions are {newTilePositions}")
                        # 250 = 2m 250k likely a day
                        if (sampleMax == True):
                            for count in range(sampleSize):
                                # Now working with solution list so need length                                
                                limitedRunList, runCount = EternityMCTS.fullSolutionCheckWithSwap(256, countLimit, testList.copy(), MCTSPosition.copy(), useHints)
                                if (len(limitedRunList) >= 200):                                    
                                    print(f"200+ solution reached of \n{limitedRunList}")
                                    file2.write(f"200+ solution reached of \n{limitedRunList}\n")
                                    print(f"The solution of {len(limitedRunList)} has been used to create new Q table values in later iterations but with no visitCount\n")
                                    interimList = limitedRunList.copy()[:88]
                                    while(len(interimList) > len(testList)):
                                        itemFound = False
                                        for item in Q:                   
                                            if interimList == item[0]:
                                                item[1] = max(item[1],len(limitedRunList))
                                                itemFound = True
                                                break
                                        # Using zero rather than one to indicate it has not been visited or solved
                                        if (itemFound == False):
                                            Q.append([interimList.copy(), len(limitedRunList), 0])
                                        interimList.pop()
                                    interimList.clear()
                                a.append(len(limitedRunList))
                                runLength.append(runCount)                                
                            print("The distribution for runs is as follows:")
                            print(sorted(Counter(a).items())) 
                            print(sorted(Counter(runLength).items()))
                            #file1.write(f"{Counter(a)}\n")
                            average = sum(a)/len(a)
                            maximum = max(Counter(a))
                            print(f"The average is {average:.5f} and maximum was {maximum}")
                            # Extremely long section to deal with 173 and 233 edge cases of double rotation
                            # As these tiles are not rotated yet, it's taking default position which is misleading
                            # Need to force alignment first
                            if (tile == 173 or tile == 233 or tile == 199):
                                #tilePositions = EternityMCTS.tileAlignment(testList)                                
                                northMatch = MCTSPosition[-1][0]
                                eastMatch = MCTSPosition[-1][1]
                                southMatch = MCTSPosition[-1][2]
                                westMatch = MCTSPosition[-1][3]
                                print(f"Current tile is {tile} with position {MCTSPosition[-1]}")
                                file1.write(f"Current tile is {tile} with position {MCTSPosition[-1]}\n")
                                if (southMatch == westMatch):
                                    print("Second potential rotation needs to be tested\n")
                                    file1.write("Second potential rotation needs to be tested\n")
                                    # Rotation is clockwise
                                    if (southMatch == eastMatch):
                                        CreateTile.rotatePosition(-1, MCTSPosition)
                                    else:
                                        CreateTile.rotatePosition(-1, MCTSPosition)
                                        CreateTile.rotatePosition(-1, MCTSPosition)
                                        CreateTile.rotatePosition(-1, MCTSPosition)
                                    print(f"The new position is {MCTSPosition[-1]}\n")
                                    file1.write(f"The new position is {MCTSPosition[-1]}\n")
                                    b = []
                                    runLength.clear()
                                    for count in range(sampleSize):
                                        limitedRunList, runCount = EternityMCTS.fullSolutionCheckWithSwap(256, countLimit, testList.copy(), MCTSPosition.copy(), useHints)
                                        if (len(limitedRunList) >= 200):                                    
                                            print(f"200+ solution reached of \n{limitedRunList}")
                                            file2.write(f"200+ solution reached of \n{limitedRunList}")
                                            print(f"The solution of {len(limitedRunList)} has been used to create new Q table values in later iterations but with no visitCount\n")
                                            interimList = limitedRunList.copy()[:88]
                                            while(len(interimList) > len(testList)):
                                                itemFound = False
                                                for item in Q:                   
                                                    if interimList == item[0]:
                                                        item[1] = max(item[1],len(limitedRunList))
                                                        itemFound = True
                                                        break
                                                # Using zero rather than one to indicate it has not been visited or solved
                                                if (itemFound == False):
                                                    Q.append([interimList.copy(), len(limitedRunList), 0])
                                                interimList.pop()
                                            interimList.clear()
                                        b.append(len(limitedRunList))
                                        runLength.append(runCount)                                        
                                    print("The distribution for the second run is as follows:")
                                    print(sorted(Counter(b).items())) # See if this works
                                    print(sorted(Counter(runLength).items()))
                                    file1.write(f"{Counter(b)}\n")
                                    average2 = sum(b)/len(b)
                                    maximum2 = max(Counter(b))
                                    print(f"The average is {average2:.5f} and maximum was {maximum2}")
                                    if (maximum2 > maximum):
                                        print(f"The second rotation was better and is being used")
                                        maximum = maximum2
                                        average = average2
                                        # Need to ensure that tileList from which option is subsequently picked is correctly updated
                                        # Would be better if options all had positions as well as tile numbers
                                        CreateTile.tileList[tile][0] = MCTSPosition[-1][0]
                                        CreateTile.tileList[tile][1] = MCTSPosition[-1][1]
                                        CreateTile.tileList[tile][2] = MCTSPosition[-1][2]
                                        CreateTile.tileList[tile][3] = MCTSPosition[-1][3]
                                    else:
                                        print(f"The first rotation was better or the same and is being used")
                                        maximum2 = maximum
                                        average2 = average
                                        eastMatch = MCTSPosition[-1][1]
                                        southMatch = MCTSPosition[-1][2]
                                        # better to use revised S and E here - less confusing
                                        if (southMatch == eastMatch):
                                            CreateTile.rotatePosition(-1, MCTSPosition)
                                        else:
                                            CreateTile.rotatePosition(-1, MCTSPosition)
                                            CreateTile.rotatePosition(-1, MCTSPosition)
                                            CreateTile.rotatePosition(-1, MCTSPosition)
                                    b = []
                                    northMatch = MCTSPosition[-1][0]
                                    eastMatch = MCTSPosition[-1][1]
                                    southMatch = MCTSPosition[-1][2]
                                    westMatch = MCTSPosition[-1][3]
                                    # Need to ensure that tileList from which option is subsequently picked is correctly updated
                                    # Would be better if options all had positions as well as tile numbers
                                    CreateTile.tileList[tile][0] = northMatch
                                    CreateTile.tileList[tile][1] = eastMatch
                                    CreateTile.tileList[tile][2] = southMatch
                                    CreateTile.tileList[tile][3] = westMatch
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
                        MCTSPosition.pop()
                        a.clear()
                        runLength.clear()
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
                        MCTSPosition = EternityMCTS.tileAlignmentOnLastPosition(MCTSList, MCTSPosition)
                    else:
                        epsilonMaxOption = options[epsilonMaxList.index(max(epsilonMaxList))]
                        MCTSList.append(epsilonMaxOption)
                        MCTSPosition.append(CreateTile.tileList[epsilonMaxOption].copy())
                        MCTSPosition = EternityMCTS.tileAlignmentOnLastPosition(MCTSList, MCTSPosition)
                    #print(f"The maximum AVERAGE was {max(averageList)} so option {maxOption} was chosen and tree search is {MCTSList}\n")
                    if (sampleMax == True):
                        print(f"The maximum VALUE using SAMPLING was {max(maxList)} so option {maxOption} was chosen with position {MCTSPosition[-1]} and tree search is {MCTSList}")
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
                        print(f"The maximum VALUE using GREEDY MAX was {max(epsilonMaxList)} so option {epsilonMaxOption} was chosen with position {MCTSPosition[-1]} and tree search is {MCTSList}")
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
                    MCTSPosition = EternityMCTS.tileAlignmentOnLastPosition(MCTSList, MCTSPosition)
                    print(f"Only a single option {options[0]} so no random samples undertaken\n")
                    #print(f"TEMP Line 267: testPosition for single option with alignment is: {testPosition}")
                    if (maximaList != []):
                        maximaList.append(maximaList[-1])
                elif (maxList == []):
                    terminalState = True
                    print(f"\nFinal tree length was {len(MCTSList)} which was \n{MCTSList}")
                    maxMCTS = MCTSList.copy() # just in case MCTS does not reach 88
                    file2.write(f"\nFinal tree length was {len(MCTSList)} which was \n{MCTSList}\n")
                    file1.write(f"\nFinal tree length was: {len(MCTSList)}\n")
                    finalLength = len(MCTSList)
                #tilePositions = EternityMCTS.tileAlignment(testList)
                #MCTSPosition = EternityMCTS.tileAlignmentOnPositions(MCTSList, MCTSPosition) - already done
                averageList.clear()
                maxList.clear()
                epsilonMaxList.clear()
                testList = MCTSList.copy()
            # New sense check - will become alternate full solution test after iteration 88 but not working atm
            verificationList = MCTSList.copy()
            verificationPositions = MCTSPosition.copy()
            #print(f"TEMP ln 285: verification list and positions are \n{verificationList}\n{verificationPositions}")
            if (len(verificationList) >= cutoff):
                cutoff = 256 # full solution test
                print (f"\nUndertaking full solution sense check with cutoff of {cutoff}\n") 
                countLimit = 5000000000
                maxMCTS, runCount = EternityMCTS.fullSolutionCheckWithSwap(cutoff, countLimit, verificationList.copy()[:88], verificationPositions.copy()[:88], useHints)
                cutoff = 88# back to sample check for future episodes
                finalLength = len(maxMCTS)
                countLimit = CreateTile.firstCountLimit
                print("FINAL RESULTS")
                print(f"Length of final solution was {finalLength} and counts required were {runCount}\n")
                print(f"The solution was\n{maxMCTS}")
                file2.write(f"Final solution from {cutoff} iteration was of length {finalLength} and the solution itself was:\n{maxMCTS}\n")
            print(f"The length of the final Q-table with state, maximum, visitcount was {len(Q)}\n")
            print(f"The lookahead for each iteration for sample size {sampleSize} and count {countLimit} was {maximaList} and maximum was {max(maximaList)} with average {sum(maximaList)/len(maximaList):.3f}\n")
            file1.write(f"The lookahead for each iteration for sample size {sampleSize} and count {countLimit} was {maximaList} and maximum was {max(maximaList)} with average {sum(maximaList)/len(maximaList):.3f}\n")
            file1.write(f"Final Q-table length: {len(Q)}\n\n\n")
            file2.write(f"The lookahead for each iteration for sample size {sampleSize} and count {countLimit} was {maximaList} and maximum was {max(maximaList)} with average {sum(maximaList)/len(maximaList):.3f}\n")
            end = time.time()
            file2.write(f"Time taken for the complete run was: {end - start:.3f} seconds\n")
            file2.write(f"Final Q-table length: {len(Q)}\n")
            print(f"Time taken for the complete run was: {end - start:.3f} seconds\n")
            episodeList.append(len(maxMCTS)) 
            MCTSList = verificationList.copy()[:cutoff]
            while(MCTSList != []):
                itemFound = False
                for item in Q:                   
                    if MCTSList == item[0]:
                        item[1] = max(item[1],finalLength)
                        itemFound = True
                        break
                # Should add to Q even for single options where no sampling was previously done (but not past cutoff) - may happen for single options
                if (itemFound == False):
                    Q.append([MCTSList.copy(), finalLength, 1])
                MCTSList.pop()
            print(f"The final length of {finalLength} has been used to update all prior Q table values\n")
            print(f"Shortened form for information of initial, average, final and time: {max(maximaList)} {sum(maximaList)/len(maximaList):.3f} {finalLength} {end-start:.0f}\n")
            file2.write(f"Shortened Form: {max(maximaList)} {sum(maximaList)/len(maximaList):.3f} {finalLength} {end-start:.0f}\n\n")
            # Final update for original leaf
            Q[0][1] = max(Q[0][1],finalLength)
            Q[0][2] = Q[0][2] + 1
            # Do Not Use if Testing
            with open("Q-table.txt","w") as handler:
                json.dump(Q,handler) 
            handler.close()             
            episode += 1    
            optionsCount = 0
        print(f"\nFor the {episode - 1} episodes run with sample size {sampleSize} and count {countLimit} the longest run was {max(episodeList)}")
        print(f"\nThe longest recorded run in the Q-Table is {Q[0][1]}")
        file1.close()

    main()



