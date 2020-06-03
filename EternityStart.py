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
        term = False # graceful way to end program where empty list
        CreateTile.createTile()
        CreateTile.findPatternMatches()
        while (len(MCTSList) <= cutoff and term == False):
            options = EternityMCTS.findNextMatches(MCTSList,True)
            random.shuffle(options)
            print(f"The new options would be {options} and the length is {len(options)}")
            for tile in options:
                testList.append(tile)
                print(f"\nThe test list is {testList}")
                tilePositions = EternityMCTS.tileAlignment(testList)
                #print(f"TEMP: The tile positions are {tilePositions}")
                for count in range(100000):
                    runLength = EternityMCTS.startMatching(testList)
                    a.append(runLength)
                    testList = MCTSList.copy()
                    testList.append(tile)
                print("The distribution for runs is as follows:")
                print(Counter(a))
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
            #maxOption = options[averageList.index(max(averageList))]
            if (maxList != []):
                maxOption = options[maxList.index(max(maxList))]
                MCTSList.append(maxOption)
                testList = MCTSList.copy()
                #print(f"The maximum AVERAGE was {max(averageList)} so option {maxOption} was chosen and tree search is {MCTSList}\n")
                print(f"The maximum VALUE was {max(maxList)} so option {maxOption} was chosen and tree search is {MCTSList}\n")
                print(f"The length of the tree search is {len(MCTSList)}")
            else:
                term = True
            tilePositions = EternityMCTS.tileAlignment(testList)
            averageList.clear()
            maxList.clear()
        
    main()



