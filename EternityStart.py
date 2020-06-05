from CreateTile import CreateTile
from EternityMCTS import EternityMCTS
from collections import Counter
import numpy as np
import time
import random

class EternityStart():
    def main():
        start = time.time()
        cutoff = 256
        MCTSList = []
        testList = []
        averageList = []
        maxList = []
        a = []
        Qs = [] # Q table with state and maximum amount
        term = False # graceful way to end program where empty list
        file = open("MCTS.txt", "w") # normally append "a" but overwriting for one turn
        CreateTile.createTile()
        CreateTile.findPatternMatches()
        while (len(MCTSList) <= cutoff and term == False):
            options = EternityMCTS.findNextMatches(MCTSList,True)
            random.shuffle(options)
            print(f"The new options would be {options} and the length is {len(options)}")
            file.write(f"{options}\n")
            for tile in options:
                testList.append(tile)
                print(f"\nThe test list is {testList}")
                tilePositions = EternityMCTS.tileAlignment(testList)
                #print(f"TEMP: The tile positions are {tilePositions}")
                # 250 = 2m 250k likely a day
                for count in range(250):
                    runLength = EternityMCTS.startMatching(testList)
                    a.append(runLength)
                    testList = MCTSList.copy()
                    testList.append(tile)
                print("The distribution for runs is as follows:")
                print(Counter(a))
                file.write(f"{Counter(a)}\n")
                average = sum(a)/len(a)
                maximum = max(Counter(a))
                print(f"The average is {average:.5f} and maximum was {maximum}")
                averageList.append(average)
                maxList.append(maximum)
                testList = MCTSList.copy()
                a.clear()
                end = time.time()
                print(f"Time taken so far is: {end - start:.3f} seconds")
            print(f"\nFor options {options}")
            # Choice of using average list or maximum list
            print(f"The averages were {averageList} and maxima were {maxList}")
            if (maxList != []):
                maxOption = options[maxList.index(max(maxList))]
                #maxOption = options[averageList.index(max(averageList))]
                MCTSList.append(maxOption)
                testList = MCTSList.copy()
                #print(f"The maximum AVERAGE was {max(averageList)} so option {maxOption} was chosen and tree search is {MCTSList}\n")
                print(f"The maximum VALUE was {max(maxList)} so option {maxOption} was chosen and tree search is {MCTSList}")
                print(f"The length of the tree search is {len(MCTSList)}")
                file.write(f"{averageList}   {maxList}\n{MCTSList}\n\n")
            else:
                term = True
                print(f"\nFinal tree length was {len(MCTSList)} which was \n{MCTSList}")
            tilePositions = EternityMCTS.tileAlignment(testList)
            averageList.clear()
            maxList.clear()
        file.close()
    main()



