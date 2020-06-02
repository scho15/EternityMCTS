from CreateTile import CreateTile
from EternityMCTS import EternityMCTS

class EternityStart():
    def main():
        # Input iteration at which cutoff should occur
        cut = 220
        CreateTile.createTile()
        CreateTile.findPatternMatches()
        EternityMCTS.startMatching(cut)
    main()



