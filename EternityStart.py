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
        start = time.time()
        maxEpisodes = 1
        sampleSize = 1000 #(250x5 is 5 mins;10K=22s per step
        episode = 1
        cutoff = 256
        Q = [] # Q list table with state and maximum amount for that state [1] and number of visits [2]
        currentVisitCount = 0
        terminalState = False # graceful way to end program where empty list
        file1 = open("MCTS.txt", "w") # normally append "a" but overwriting for one turn  
        if (os.path.isfile('Q-Table.txt') == True):
            with open("Q-table.txt", "r") as QTablefile:
                Q = json.load(QTablefile)
            print(f"Q-table uploaded with {len(Q)} lines")
        CreateTile.createTile()
        CreateTile.findPatternMatches()
        episodeList = [] # list if episode lengths
        while episode <= maxEpisodes:
            MCTSList = []
            testList = []
            averageList = []
            maxList = []
            epsilonMaxList = []
            a = []
            terminalState = False
            while (len(MCTSList) <= cutoff and terminalState == False):
                options = EternityMCTS.findNextMatches(MCTSList,True)
                if len(options) != len(set(options)):
                    print("There are DUPLICATE options to deal with NOT YET PROGRAMMED\n")
                    file1.write("There are DUPLICATE options to deal with NOT YET PROGRAMMED\n")
                    duplicate = True
                if (173 in options):
                    file1.write("ROTATION: This list contains tile 173 that may have two positions\n")
                if (233 in options):
                    file1.write("ROTATION: This list contains tile 233 that may have two positions\n")
                random.shuffle(options)
                print(f"The new options would be {options} and the length is {len(options)}")
                file1.write(f"{options}\n")
                if (len(options) > 1):
                    for item in Q:
                        if MCTSList == item[0]:
                            currentVisitCount = item[2]
                    epsilon = 1000/ (1000 + currentVisitCount)		
                    print(f"Epsilon is set at {epsilon:.5f} and visitCount at {currentVisitCount}")
			        #epsilon = 1 #test out completely random policy
                    # Three options - random, sample maximum or current largest maximum as tree policy
                    # In order to learn, using sample maximum and largest maximum for tree policy and avoiding random
                    if (random.random() < epsilon):
                        print(f"SAMPLE: Proceeding with sample testing and using results of sample")
                        sampleMax = True
                    else:
                        print(f"GREEDY: Taking the current largest maximum value including this sample test")
                        sampleMax = False
                    for tile in options:
                        itemFound = False
                        testList.append(tile)
                        print(f"\nThe test list is {testList}")
                        # Implicitly does not deal with tiles that can have two positions
                        tilePositions = EternityMCTS.tileAlignment(testList)
                        #print(f"TEMP: The tile positions are {tilePositions}")
                        # 250 = 2m 250k likely a day
                        for count in range(sampleSize):
                            runLength = EternityMCTS.startMatching(testList)
                            a.append(runLength)
                            testList = MCTSList.copy()
                            testList.append(tile)
                        print("The distribution for runs is as follows:")
                        print(sorted(Counter(a).items())) # See if this works
                        #print(Counter(a)) # plain Counter
                        file1.write(f"{Counter(a)}\n")
                        average = sum(a)/len(a)
                        maximum = max(Counter(a))
                        print(f"The average is {average:.5f} and maximum was {maximum}")
                        averageList.append(average)
                        maxList.append(maximum)
                        if len(Q) == 0:
                            Q.append([MCTSList.copy(),maximum,0])
                        for item in Q:  
                            #print(f"Item is {item}")
                            if testList == item[0]:
                                #print(f"item[0] is {item[0]}")
                                item[2] = item[2] + 1
                                item[1] = max(item[1],maximum)
                                epsilonMaxList.append(item[1])
                                itemFound = True
                                break;
                        if (itemFound == False):
                            #print(f"testlist {testList} is not in Q")
                            Q.append([testList.copy(), maximum, 1])
                            epsilonMaxList.append(maximum)
                        testList = MCTSList.copy()
                        a.clear()
                        end = time.time()
                        currentVisitCount = 0
                        print(f"Time taken so far is: {end - start:.3f} seconds")
                    print(f"\nFor options {options}")
                    # Choice of using average list or maximum list
                    print(f"The averages were {averageList}, sample maxima were {maxList} and greedy maxima were {epsilonMaxList}")
                    file1.write(f"Average List:\n{averageList}\nSample Maxima:\n{maxList}\nGreedy Maxima:\n{epsilonMaxList}")
                if (len(options) > 1 and maxList != []):
                    maxOption = options[maxList.index(max(maxList))]
                    epsilonMaxOption = options[epsilonMaxList.index(max(epsilonMaxList))]
                    #maxOption = options[averageList.index(max(averageList))]
                    if (sampleMax == True):
                        MCTSList.append(maxOption)
                    else:
                        MCTSList.append(epsilonMaxOption)
                    testList = MCTSList.copy()
                    #print(f"The maximum AVERAGE was {max(averageList)} so option {maxOption} was chosen and tree search is {MCTSList}\n")
                    if (sampleMax == True):
                        print(f"The maximum VALUE using SAMPLING was {max(maxList)} so option {maxOption} was chosen and tree search is {MCTSList}")
                        file1.write(f"\nThe maximum VALUE using SAMPLING was {max(maxList)} so option {maxOption} was chosen\n")
                    else:
                        print(f"The maximum VALUE using GREEDY MAX was {max(epsilonMaxList)} so option {epsilonMaxOption} was chosen and tree search is {MCTSList}")
                        file1.write(f"\nThe maximum VALUE using GREEDY MAX was {max(epsilonMaxList)} so option {epsilonMaxOption} was chosen\n")
                    print(f"The length of the tree search is {len(MCTSList)}\n")
                    file1.write(f"The length of the tree search is {len(MCTSList)}\n")
                    file1.write(f"{MCTSList}\n\n")
                elif (len(options) == 1):
                    MCTSList.append(options[0])
                    testList = MCTSList.copy()
                    print(f"Only a single option {options[0]} so no random samples undertaken\n")
                elif (maxList == []):
                    terminalState = True
                    print(f"\nFinal tree length was {len(MCTSList)} which was \n{MCTSList}")
                    file1.write(f"\nFinal tree length was: {len(MCTSList)}\n")
                    finalLength = len(MCTSList)
                tilePositions = EternityMCTS.tileAlignment(testList)
                currentVisitCount = 0
                averageList.clear()
                maxList.clear()
                epsilonMaxList.clear()
            #print(f"\nFinal Q-table with state, maximum, visitcount was\n {Q}")
            print(f"The length of the final Q-table with state, maximum, visitcount was {len(Q)}")
            file1.write(f"Final Q-table length: {len(Q)}\n\n\n")
            episodeList.append(len(MCTSList))
            while(MCTSList != []):
                for item in Q:                   
                    if MCTSList == item[0]:
                        item[1] = max(item[1],finalLength)
                MCTSList.pop()
            print(f"The final length has been used to update all prior Q table values")
            # Final update for original leaf
            Q[0][1] = max(Q[0][1],finalLength)
            Q[0][2] = Q[0][2] + 1
            with open("Q-table.txt","w") as handler:
                json.dump(Q,handler)           
            episode += 1
        print(f"\nFor the {episode - 1} episodes run with sample size {sampleSize} the longest run was {max(episodeList)}")
        print(f"\nThe longest recorded run in the Q-Table is {Q[0][1]}")
        file1.close()
        handler.close()

    main()



