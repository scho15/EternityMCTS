from CreateTile import CreateTile
from EternityMCTS import EternityMCTS
from collections import Counter
import numpy as np
import time

class EternityStart():
    def main():
        start = time.time()
        testList = []
        a = []
        CreateTile.createTile()
        CreateTile.findPatternMatches()
        options = EternityMCTS.findNextMatches([],True)
        print(f"The new options would be {options} and the length is {len(options)}")
        for tile in options:
            testList.append(tile)
            print(f"\nThe test list is {testList}")
            tilePositions = EternityMCTS.tileAlignment(testList)
            for count in range(1000):
                runLength = EternityMCTS.startMatching(testList)
                a.append(runLength)
                testList.clear()
                testList.append(tile)
            print("The distribution for runs is as follows:")
            print(Counter(a))
            print(f"The average is {sum(a)/len(a):.5f}")
            testList.clear()
            a.clear()
            end = time.time()
            print(f"Time taken so far is: {end - start:.3f} seconds")
    
    main()

# Functions Required
# Convert usedTilelist to tilelist in correct position

