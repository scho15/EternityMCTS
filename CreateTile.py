import random

class CreateTile():
    # Reduced tile list also produced taking into account used tiles
    tileList = [] # Create list of tiles with index tilenumber and edges as 4 properties

    PATTERN_TYPES = 22
    TILE_SET_SIZE = 256
    tilePatternSet = set()
    tilePatternList = [] # List of tiles with tile patterns    
    twoTilePatternSet = set()
    twoTilePatternList = []
    twoPatternList = []
    detailedPatternList = []  
    
    reducedSet = set() # set without input tiles
    reducedList = [] # list without input tiles
    twoReducedTileSet = set()
    twoReducedTileList = []
    twoReducedList = []
    detailedReducedList = []
    
    detailedThreePatternList = []
    detailedThreeReducedList = []

    #doubleRotation = [False, False, False]
    #firstCountLimit = 0
    #terminalCountLimit = 0

    def createTile():       
        # 0: Grey edge tile
        # 1: Pink/Light Blue - like swallow
        # 2: Dk Blue/Yellow - 4 pointed cross, club style
        # 3: Orange/Lt Blue - Cross style
        # 4: Green/Dk Blue - Hexagon
        # 5: Brown/Orange - Castle style
        # Middle Area Tiles
        # 6: Dk Blue/Orange - cross with club feet
        # 7: Dk Blue/Pink - dark blue cross in pink circle
        # 8: Dk Blue/Lt Blue - Diamond
        # 9: Orange/Purple - 6 pointed star
        # 10: Green/Orange - 4 pointed flared cross
        # 11: Green/Pink - 4 pointed cross club style
        # 12: Brown/Green - Brown cross in green circle
        # 13: Brown/Yellow - 6 pointed star
        # 14: Pink/Yellow - 4 pointed cross club style
        # 15: Pink/Yellow - 4 pointed castle style
        # 16: Purple/Lt Blue - 4 pointed flared cross
        # 17: Purple/Yellow - purple cross in yellow circle
        # 18: Yellow/Green - Diamond
        # 19: Yellow/Mid Blue - 6 pointed star
        # 20: Yellow/Blue - 4 pointed cross castle style
        # 21: Lt Blue/Pink - 4 pointed flared cross
        # 22: Lt Blue/Pink - 4 pointed cross castle style

        # Create set of Eternity tiles
        CreateTile.tileList.insert(0, [-1, -1, -1, -1])
        CreateTile.tileList.insert(1, [3, 1, 0, 0])
        CreateTile.tileList.insert(2, [3, 4, 0, 0])
        CreateTile.tileList.insert(3, [2, 1, 0, 0])
        CreateTile.tileList.insert(4, [1, 2, 0, 0])
        CreateTile.tileList.insert(5, [3, 14, 3, 0])
        CreateTile.tileList.insert(6, [3, 16, 2, 0])
        CreateTile.tileList.insert(7, [3, 17, 3, 0])
        CreateTile.tileList.insert(8, [3, 17, 5, 0 ])
        CreateTile.tileList.insert(9, [3, 10, 1, 0 ])
        CreateTile.tileList.insert(10, [3, 22, 4, 0 ])
        CreateTile.tileList.insert(11, [3, 18, 2, 0 ])
        CreateTile.tileList.insert(12, [3, 6 , 4, 0 ])
        CreateTile.tileList.insert(13, [3, 6 , 5, 0 ])
        CreateTile.tileList.insert(14, [3, 15, 4, 0 ])
        CreateTile.tileList.insert(15, [2, 16, 3, 0 ])
        CreateTile.tileList.insert(16, [2, 19, 1, 0 ])
        CreateTile.tileList.insert(17, [2, 11, 5, 0 ])
        CreateTile.tileList.insert(18, [2, 13, 5, 0 ])
        CreateTile.tileList.insert(19, [2, 22, 2, 0 ])
        CreateTile.tileList.insert(20, [2, 18, 2, 0 ])
        CreateTile.tileList.insert(21, [2, 21, 4, 0 ])
        CreateTile.tileList.insert(22, [2, 20, 3, 0 ])
        CreateTile.tileList.insert(23, [2, 20, 5, 0 ])
        CreateTile.tileList.insert(24, [2, 9 , 3, 0 ])
        CreateTile.tileList.insert(25, [2, 15, 3, 0 ])
        CreateTile.tileList.insert(26, [1, 14, 2, 0 ])
        CreateTile.tileList.insert(27, [1, 14, 1, 0 ])
        CreateTile.tileList.insert(28, [1, 16, 1, 0 ])
        CreateTile.tileList.insert(29, [1, 19, 1, 0 ])
        CreateTile.tileList.insert(30, [1, 22, 5, 0 ])
        CreateTile.tileList.insert(31, [1, 18, 2, 0 ])
        CreateTile.tileList.insert(32, [1, 9 , 1, 0 ])
        CreateTile.tileList.insert(33, [1, 6 , 2, 0 ])
        CreateTile.tileList.insert(34, [1, 6 , 4, 0 ])
        CreateTile.tileList.insert( 35,[1, 8 , 5, 0 ])
        CreateTile.tileList.insert( 36,[1, 7 , 4, 0 ])
        CreateTile.tileList.insert( 37, [4, 19, 3, 0 ])
        CreateTile.tileList.insert( 38, [4, 12, 5, 0 ])
        CreateTile.tileList.insert( 39, [4, 10, 5, 0 ])
        CreateTile.tileList.insert( 40, [4, 13, 2, 0 ])
        CreateTile.tileList.insert( 41, [4, 13, 1, 0 ])
        CreateTile.tileList.insert( 42, [4, 18, 3, 0 ])
        CreateTile.tileList.insert( 43, [4, 18, 2, 0 ])
        CreateTile.tileList.insert( 44, [4, 18, 1, 0 ])
        CreateTile.tileList.insert( 45, [4, 21, 3, 0 ])
        CreateTile.tileList.insert( 46, [4, 9 , 4, 0 ])
        CreateTile.tileList.insert( 47, [4, 6 , 4, 0 ])
        CreateTile.tileList.insert( 48, [4, 8 , 4, 0 ])
        CreateTile.tileList.insert( 49, [5, 14, 5, 0 ])
        CreateTile.tileList.insert( 50, [5, 16, 3, 0 ])
        CreateTile.tileList.insert( 51, [5, 16, 2, 0 ])
        CreateTile.tileList.insert( 52, [5, 17, 3, 0 ])
        CreateTile.tileList.insert( 53, [5, 22, 4, 0 ])
        CreateTile.tileList.insert( 54, [5, 21, 4, 0 ])
        CreateTile.tileList.insert( 55, [5, 21, 5, 0 ])
        CreateTile.tileList.insert( 56, [5, 6 , 1, 0 ])
        CreateTile.tileList.insert( 57, [5, 8 , 3, 0 ])
        CreateTile.tileList.insert( 58, [5, 8 , 5, 0 ])
        CreateTile.tileList.insert( 59, [5, 15, 2, 0 ])
        CreateTile.tileList.insert( 60, [5, 7 , 1, 0 ])
        CreateTile.tileList.insert( 61, [17, 19, 14, 14 ])
        CreateTile.tileList.insert( 62, [11, 22, 14, 14 ])
        CreateTile.tileList.insert( 63, [16, 12, 14, 16 ])
        CreateTile.tileList.insert( 64, [14, 6 , 14, 19 ])
        CreateTile.tileList.insert( 65, [19, 7 , 14, 19 ])
        CreateTile.tileList.insert( 66, [11, 11, 14, 19 ])
        CreateTile.tileList.insert( 67, [10, 16, 14, 19 ])
        CreateTile.tileList.insert( 68, [9 , 17, 14, 19 ])
        CreateTile.tileList.insert( 69, [7 ,  6, 14, 19 ])
        CreateTile.tileList.insert( 70, [12, 22, 14, 12 ])
        CreateTile.tileList.insert( 71, [22, 20, 14, 12 ])
        CreateTile.tileList.insert( 72, [11, 19, 14, 10 ])
        CreateTile.tileList.insert( 73, [18, 21, 14, 10 ])
        CreateTile.tileList.insert( 74, [9 , 18, 14, 10 ])
        CreateTile.tileList.insert( 75, [6 , 12, 14, 10 ])
        CreateTile.tileList.insert( 76, [11, 18, 14, 13 ])
        CreateTile.tileList.insert( 77, [13, 18, 14, 13 ])
        CreateTile.tileList.insert( 78, [12,  8, 14, 22 ])
        CreateTile.tileList.insert( 79, [9 , 12, 14, 22 ])
        CreateTile.tileList.insert( 80, [8 , 15, 14, 22 ])
        CreateTile.tileList.insert( 81, [13, 19, 14, 18 ])
        CreateTile.tileList.insert( 82, [19, 19, 14, 21 ])
        CreateTile.tileList.insert( 83, [10, 21, 14, 21 ]) 
        CreateTile.tileList.insert( 84, [19, 13, 14, 20 ])
        CreateTile.tileList.insert( 85, [17, 11, 14, 20 ])
        CreateTile.tileList.insert( 86, [6 , 20, 14, 20 ])
        CreateTile.tileList.insert( 87, [8 , 9 , 14, 20 ])
        CreateTile.tileList.insert( 88, [14, 15, 14,  9 ])
        CreateTile.tileList.insert( 89, [17, 7 , 14,  9 ])
        CreateTile.tileList.insert( 90, [21, 8 , 14,  9 ])
        CreateTile.tileList.insert( 91, [10, 20, 14,  6 ])
        CreateTile.tileList.insert( 92, [13, 18, 14,  6 ])
        CreateTile.tileList.insert( 93, [13, 21, 14,  6 ])
        CreateTile.tileList.insert( 94, [21, 15, 14,  6 ])
        CreateTile.tileList.insert( 95, [20, 11, 14,  6 ])
        CreateTile.tileList.insert( 96, [15, 12, 14, 15 ])
        CreateTile.tileList.insert( 97, [21, 13, 14,  7 ])
        CreateTile.tileList.insert( 98, [9,  6, 14,  7 ])
        CreateTile.tileList.insert( 99, [15, 17, 14,  7 ])
        CreateTile.tileList.insert( 100, [7, 15, 14, 7 ])
        CreateTile.tileList.insert( 101, [20, 18, 16, 16 ])
        CreateTile.tileList.insert( 102, [20,  8, 16, 16 ])
        CreateTile.tileList.insert( 103, [8, 13, 16, 16 ])
        CreateTile.tileList.insert( 104, [7, 17, 16, 16 ])
        CreateTile.tileList.insert( 105, [21, 18, 16, 19 ])
        CreateTile.tileList.insert( 106, [12,  6, 16, 17 ])
        CreateTile.tileList.insert( 107, [13,  6, 16, 17 ])
        CreateTile.tileList.insert( 108, [21, 18, 16, 17 ])
        CreateTile.tileList.insert( 109, [8, 10, 16, 17 ])
        CreateTile.tileList.insert( 110, [18, 20, 16, 11 ])
        CreateTile.tileList.insert( 111, [20, 18, 16, 11 ])
        CreateTile.tileList.insert( 112, [9, 13, 16, 12 ])
        CreateTile.tileList.insert( 113, [9,  8, 16, 12 ])
        CreateTile.tileList.insert( 114, [11, 21, 16, 10 ])
        CreateTile.tileList.insert( 115, [22, 20, 16, 10 ]) 
        CreateTile.tileList.insert( 116, [20, 10, 16, 10 ])
        CreateTile.tileList.insert( 117,  [7,  8, 16, 10 ])
        CreateTile.tileList.insert( 118, [12, 15, 16, 13 ])
        CreateTile.tileList.insert( 119,  [8, 20, 16, 22 ]) 
        CreateTile.tileList.insert( 120,  [6,  7, 16, 18 ])
        CreateTile.tileList.insert( 121, [11,  7, 16, 21 ]) 
        CreateTile.tileList.insert( 122, [17,  8, 16,  9 ])
        CreateTile.tileList.insert( 123, [11, 13, 16,  9 ])
        CreateTile.tileList.insert( 124,  [9, 18, 16,  9 ])
        CreateTile.tileList.insert( 125, [20,  7, 16,  6 ])
        CreateTile.tileList.insert( 126, [15, 18, 16,  6 ])
        CreateTile.tileList.insert( 127, [11, 17, 16,  8 ])
        CreateTile.tileList.insert( 128, [13, 15, 16,  8 ])
        CreateTile.tileList.insert( 129, [21, 12, 16,  8 ])
        CreateTile.tileList.insert( 130,  [9,  6, 16,  8 ])
        CreateTile.tileList.insert( 131, [17,  9, 16, 15 ])
        CreateTile.tileList.insert( 132, [20, 11, 16, 15 ])
        CreateTile.tileList.insert( 133, [11,  8, 16,  7 ])
        CreateTile.tileList.insert( 134, [10, 21, 16,  7 ])
        CreateTile.tileList.insert( 135, [21, 12, 16,  7 ]) 
        CreateTile.tileList.insert( 136,  [8,  9, 16,  7 ])
        CreateTile.tileList.insert( 137,  [9, 22, 19, 19 ])
        CreateTile.tileList.insert( 138, [17, 12, 19, 17 ])
        CreateTile.tileList.insert( 139, [19, 17, 17, 10 ]) # centre tile with 19 top N in pos 120
        CreateTile.tileList.insert( 140, [17, 20, 19, 17 ])
        CreateTile.tileList.insert( 141, [13, 15, 19, 17 ])
        CreateTile.tileList.insert( 142, [18, 17, 19, 17 ])
        CreateTile.tileList.insert( 143,  [8, 20, 19, 17 ]) 
        CreateTile.tileList.insert( 144, [15, 15, 19, 17 ])
        CreateTile.tileList.insert( 145, [12, 21, 19, 11 ])
        CreateTile.tileList.insert( 146, [19, 20, 19, 12 ])
        CreateTile.tileList.insert( 147, [19,  7, 19, 12 ])
        CreateTile.tileList.insert( 148, [12, 11, 19, 12 ])
        CreateTile.tileList.insert( 149, [18, 20, 19, 12 ])
        CreateTile.tileList.insert( 150, [17, 10, 19, 13 ])
        CreateTile.tileList.insert( 151, [21,  7, 19, 13 ])
        CreateTile.tileList.insert( 152, [10, 10, 19, 22 ])
        CreateTile.tileList.insert( 153, [10, 13, 19, 22 ])
        CreateTile.tileList.insert( 154,  [7,  8, 19, 22 ])
        CreateTile.tileList.insert( 155, [22, 22, 19, 21 ])
        CreateTile.tileList.insert( 156, [22, 20, 19, 21 ])
        CreateTile.tileList.insert( 157,  [7, 22, 19, 21 ])
        CreateTile.tileList.insert( 158, [22,  8, 19,  9 ])
        CreateTile.tileList.insert( 159,  [6, 17, 19,  9 ])
        CreateTile.tileList.insert( 160, [15, 15, 19,  6 ])
        CreateTile.tileList.insert( 161, [17,  9, 19,  8 ])
        CreateTile.tileList.insert( 162, [11,  9, 19,  8 ])
        CreateTile.tileList.insert( 163, [18, 10, 19,  7 ])
        CreateTile.tileList.insert( 164, [21,  8, 19,  7 ])
        CreateTile.tileList.insert( 165, [12, 21, 17, 11 ])
        CreateTile.tileList.insert( 166, [21,  6, 17, 11 ])
        CreateTile.tileList.insert( 167, [12, 12, 17, 10 ])
        CreateTile.tileList.insert( 168, [10, 18, 17, 13 ])
        CreateTile.tileList.insert( 169, [13, 15, 17, 13 ])
        CreateTile.tileList.insert( 170, [21,  6, 17, 22 ])
        CreateTile.tileList.insert( 171,  [9,  8, 17, 22 ])
        CreateTile.tileList.insert( 172, [15, 10, 17, 22 ])
        CreateTile.tileList.insert( 173, [18, 18, 17, 18 ])
        CreateTile.tileList.insert( 174, [20,  9, 17, 18 ])
        CreateTile.tileList.insert( 175, [22, 15, 17, 21 ]) 
        CreateTile.tileList.insert( 176, [22, 13, 17, 20 ])
        CreateTile.tileList.insert( 177, [11, 21, 17,  9 ])
        CreateTile.tileList.insert( 178, [20,  8, 17,  6 ])
        CreateTile.tileList.insert( 179,  [6, 18, 17,  6 ])
        CreateTile.tileList.insert( 180, [22,  8, 17,  8 ])
        CreateTile.tileList.insert( 181, [10,  8, 17, 15 ]) # posn N3 (SW so 35) with 8 [diamond) N
        CreateTile.tileList.insert( 182, [22, 10, 17, 15 ])
        CreateTile.tileList.insert( 183, [13,  6, 11, 11 ])
        CreateTile.tileList.insert( 184,  [7, 22, 11, 12 ])
        CreateTile.tileList.insert( 185, [13, 20, 11, 10 ])
        CreateTile.tileList.insert( 186,  [6,  6, 11, 10 ])
        CreateTile.tileList.insert( 187, [15, 22, 11, 13 ])
        CreateTile.tileList.insert( 188, [11, 15, 11, 22 ])
        CreateTile.tileList.insert( 189, [12, 13, 11, 22 ])
        CreateTile.tileList.insert( 190,  [8, 13, 11, 22 ])
        CreateTile.tileList.insert( 191, [12, 12, 11, 18 ])
        CreateTile.tileList.insert( 192, [18,  9, 11, 18 ])
        CreateTile.tileList.insert( 193, [10, 22, 11, 21 ])
        CreateTile.tileList.insert( 194, [15, 10, 11, 20 ])
        CreateTile.tileList.insert( 195, [15,  7, 11, 20 ])
        CreateTile.tileList.insert( 196,  [7, 18, 11, 20 ])
        CreateTile.tileList.insert( 197, [10,  7, 11,  9 ])
        CreateTile.tileList.insert( 198, [13,  6, 11,  9 ])
        CreateTile.tileList.insert( 199,  [9,  9, 11,  9 ])
        CreateTile.tileList.insert( 200, [13, 12, 11,  6 ])
        CreateTile.tileList.insert( 201, [15,  6, 11,  8 ])
        CreateTile.tileList.insert( 202,  [7, 22, 11,  8 ])
        CreateTile.tileList.insert( 203, [20, 13, 11, 15 ])
        CreateTile.tileList.insert( 204, [20,  6, 11, 15 ])
        CreateTile.tileList.insert( 205,  [8, 12, 11, 15 ])
        CreateTile.tileList.insert( 206,  [7, 15, 11, 15 ])
        CreateTile.tileList.insert( 207,  [7, 22, 12, 12 ])
        CreateTile.tileList.insert( 208, [13,  7, 12, 10 ]) # posn C3 so 211 with 7 North
        CreateTile.tileList.insert( 209,  [6, 18, 12, 10 ])
        CreateTile.tileList.insert( 210, [10, 13, 12, 22 ])
        CreateTile.tileList.insert( 211,  [8, 18, 12, 22 ])
        CreateTile.tileList.insert( 212, [12,  8, 12, 18 ])
        CreateTile.tileList.insert( 213,  [6,  6, 12, 21 ])
        CreateTile.tileList.insert( 214, [12,  9, 12, 20 ])
        CreateTile.tileList.insert( 215, [21,  7, 12, 20 ])
        CreateTile.tileList.insert( 216,  [7, 15, 12, 20 ])
        CreateTile.tileList.insert( 217, [13, 18, 12,  9 ])
        CreateTile.tileList.insert( 218, [21, 20, 12,  8 ])
        CreateTile.tileList.insert( 219, [10, 21, 12, 15 ])
        CreateTile.tileList.insert( 220, [10,  8, 12,  7 ])
        CreateTile.tileList.insert( 221, [15, 15, 12,  7 ])
        CreateTile.tileList.insert( 222, [15,  7, 12,  7 ])
        CreateTile.tileList.insert( 223, [20,  7, 10, 10 ])
        CreateTile.tileList.insert( 224,  [9, 22, 10, 10 ])
        CreateTile.tileList.insert( 225,  [8, 18, 10, 10 ])
        CreateTile.tileList.insert( 226, [13, 18, 10, 22 ])
        CreateTile.tileList.insert( 227, [20, 20, 10, 22 ])
        CreateTile.tileList.insert( 228, [13,  6, 10, 21 ])
        CreateTile.tileList.insert( 229, [22,  7, 10,  9 ])
        CreateTile.tileList.insert( 230,  [8,  6, 10,  9 ])
        CreateTile.tileList.insert( 231, [20,  9, 10,  6 ])
        CreateTile.tileList.insert( 232, [20, 15, 10,  6 ])
        CreateTile.tileList.insert( 233, [13,  9, 13, 13 ])
        CreateTile.tileList.insert( 234, [8, 21, 13, 22 ])
        CreateTile.tileList.insert( 235, [22, 21, 13, 21 ])
        CreateTile.tileList.insert( 236, [22,  9, 13, 21 ])
        CreateTile.tileList.insert( 237, [20, 18, 13, 21 ])
        CreateTile.tileList.insert( 238, [21,  8, 13, 20 ])
        CreateTile.tileList.insert( 239, [18,  7, 13,  9 ])
        CreateTile.tileList.insert( 240, [15, 18, 13,  9 ])
        CreateTile.tileList.insert( 241, [2, 15, 13,  6 ])
        CreateTile.tileList.insert( 242, [21, 15, 13,  6 ])
        CreateTile.tileList.insert( 243, [18, 20, 22, 18 ])
        CreateTile.tileList.insert( 244,  [9,  6, 22, 18 ])
        CreateTile.tileList.insert( 245,  [7,  9, 22, 21 ])
        CreateTile.tileList.insert( 246,  [8,  7, 22, 15 ])
        CreateTile.tileList.insert( 247, [15,  7, 18, 18 ])
        CreateTile.tileList.insert( 248, [20, 21, 18, 21 ])
        CreateTile.tileList.insert( 249, [21, 15, 18, 20 ]) # pon N14 so 46 and SE with 21 N side
        CreateTile.tileList.insert( 250,  [8, 15, 18,  9 ])
        CreateTile.tileList.insert( 251,  [7,  6, 21, 21 ])
        CreateTile.tileList.insert( 252,  [6, 20, 21, 20 ])
        CreateTile.tileList.insert( 253,  [8,  9, 20,  6 ])
        CreateTile.tileList.insert( 254, [15,  8,  9,  8 ])
        CreateTile.tileList.insert( 255,  [8,  7,  9,  7 ]) # posn C14 (so 222 and NE) with 8 W side
        CreateTile.tileList.insert( 256, [15,  7,  6,  7 ])

        #print(f"tileList created with {len(CreateTile.tileList)} entries")

    def findPatternMatches(input):
        for x in range(CreateTile.PATTERN_TYPES + 1):
            for y in range(CreateTile.TILE_SET_SIZE + 1):
                for z in range( 4 ):
                    if(CreateTile.tileList[y][z] == x):
                        tileStr = str(y).zfill(3) + str(CreateTile.tileList[y][0]).zfill(2) + str(CreateTile.tileList[y][1]).zfill(2) + str(CreateTile.tileList[y][2]).zfill(2) + str(CreateTile.tileList[y][3]).zfill(2)
                        CreateTile.tilePatternSet.add(tileStr)
                        if y not in input:
                            CreateTile.reducedSet.add(tileStr)
            CreateTile.tilePatternList.append(CreateTile.tilePatternSet.copy())
            CreateTile.reducedList.append(CreateTile.reducedSet.copy())
            CreateTile.tilePatternSet.clear()
            CreateTile.reducedSet.clear()
            #print(f"Set of tiles with tile pattern {x} is {CreateTile.tilePatternList[x]} and length {len(CreateTile.tilePatternList[x])}") 
        for w in range(CreateTile.PATTERN_TYPES + 1):
            for x in range(CreateTile.PATTERN_TYPES + 1):
                for y in range(CreateTile.TILE_SET_SIZE + 1):
                    for z in range( 4 ):
                        if(CreateTile.tileList[y][z] == w and CreateTile.tileList[y][(z+1)%4] == x):
                            tileStr = str(y).zfill(3) + str(CreateTile.tileList[y][(z+2)%4]).zfill(2) + str(CreateTile.tileList[y][(z+3)%4]).zfill(2) + str(CreateTile.tileList[y][z]).zfill(2) + str(CreateTile.tileList[y][(z+1)%4]).zfill(2)
                            CreateTile.twoTilePatternSet.add(tileStr)
                            if y not in input:
                                CreateTile.twoReducedTileSet.add(tileStr)
                CreateTile.twoTilePatternList.extend(CreateTile.twoTilePatternSet.copy())
                CreateTile.twoReducedTileList.extend(CreateTile.twoReducedTileSet.copy())
                CreateTile.twoPatternList.append(CreateTile.twoTilePatternList.copy())
                CreateTile.twoReducedList.append(CreateTile.twoReducedTileList.copy())
                CreateTile.twoTilePatternSet.clear()
                CreateTile.twoReducedTileSet.clear()
                CreateTile.twoTilePatternList.clear()
                CreateTile.twoReducedTileList.clear()
            CreateTile.detailedPatternList.append(CreateTile.twoPatternList.copy())
            CreateTile.detailedReducedList.append(CreateTile.twoReducedList.copy())
            CreateTile.twoPatternList.clear()
            CreateTile.twoReducedList.clear()
        #print(f"Set of tiles with tile pattern {0} is {CreateTile.detailedPatternList[0]} and length {len(CreateTile.detailedPatternList[0])}\n")
        print(f"Test example for patterns 9 and 9 would be [9][9] {CreateTile.detailedPatternList[9][9]}")
        #print(f"REDUCED Set of tiles with tile pattern {0} is {CreateTile.detailedReducedList[0]} and length {len(CreateTile.detailedReducedList[0])}\n")
        #print(f"Test example for REDUCED patterns 9 and 9 would be [9][9] {CreateTile.detailedReducedList[9][9]}")

    # May be able to greatly simplify to return CreateTile.detailedPatternList[x][y]
    def findConsecutivePatternMatches(x, y):
            output = CreateTile.detailedPatternList[x][y].copy()            
            return output

    def findConsecutiveReducedMatches(x, y):
            output = CreateTile.detailedReducedList[x][y].copy()            
            return output

    def findThreePatternMatches(input):
        threeTilePatternList = []
        nextPatternList = []
        threeTilePatternSet = set()
        threePatternList = []
        # new to deal with tiles already used in input
        threeTileReducedList = []
        nextReducedList = []
        threeTileReducedSet = set()
        threeReducedList = []

        for a in range(CreateTile.PATTERN_TYPES + 1):
            for b in range(CreateTile.PATTERN_TYPES + 1):
                for c in range(CreateTile.PATTERN_TYPES + 1):
                    for d in range(CreateTile.TILE_SET_SIZE + 1):
                        for e in range( 4 ):
                            # rotation needs to be SWN for 104 rather than ESW
                            if(CreateTile.tileList[d][e] == a and CreateTile.tileList[d][(e+1)%4] == b and CreateTile.tileList[d][(e+2)%4] == c):
                                tileStr = str(d).zfill(3) + str(CreateTile.tileList[d][(e+3)%4]).zfill(2) + str(CreateTile.tileList[d][(e+0)%4]).zfill(2) + str(CreateTile.tileList[d][(e+1)%4]).zfill(2) + str(CreateTile.tileList[d][(e+2)%4]).zfill(2)                            
                                threeTilePatternSet.add(tileStr)
                                if d not in input:
                                    threeTileReducedSet.add(tileStr)
                    threeTilePatternList.extend(threeTilePatternSet.copy())
                    threePatternList.append(threeTilePatternList.copy())
                    threeTilePatternSet.clear()
                    threeTilePatternList.clear()
                    threeTileReducedList.extend(threeTileReducedSet.copy())
                    threeReducedList.append(threeTileReducedList.copy())
                    threeTileReducedSet.clear()
                    threeTileReducedList.clear()
                nextPatternList.append(threePatternList.copy())
                threePatternList.clear()
                nextReducedList.append(threeReducedList.copy())
                threeReducedList.clear()
            CreateTile.detailedThreePatternList.append(nextPatternList.copy())
            nextPatternList.clear()
            CreateTile.detailedThreeReducedList.append(nextReducedList.copy())
            nextReducedList.clear()
        #print(f"TEST: detailedThreePatternList[0] is {CreateTile.detailedThreePatternList[0]} and length {len(CreateTile.detailedThreePatternList[0])}")
        #print(f"TEST: Set of tiles with tile pattern 0,0 is {CreateTile.detailedThreePatternList[0][0]} and length {len(CreateTile.detailedThreePatternList[0][0])}\n")
        print(f"Example for patterns 17,17,10 would be {CreateTile.detailedThreePatternList[17][17][10]}")
        print(f"Example for patterns 19,17,17 would be {CreateTile.detailedThreePatternList[19][17][17]}")       
        print(f"Reduced example for patterns 10,8,17 would be {CreateTile.detailedThreeReducedList[10][8][17]}")

    def findThreeConsecutivePatternMatches(x, y, z):
            output = CreateTile.detailedThreePatternList[x][y][z].copy()            
            return output

    # used for iteration 104 to rotate output
    def findThreeSWNPatternMatches(x, y, z):
            output = CreateTile.detailedThreePatternList[x][y][z].copy()  
            newoutput = []
            #print(f"TEMP 417: Output is {output}")
            if (output != []):
                for tile in output:
                    newoutput.append(tile[0:3] + tile[9:11] + tile[3:5] + tile[5:7] + tile[7:9])
            #print(f"TEMP 421: Revised output is {newoutput}")
            return newoutput

    def findThreeConsecutiveReducedMatches(x, y, z):
            output = CreateTile.detailedThreeReducedList[x][y][z].copy()       
            return output

    def findTileMatches():
        for x in range(TILE_SET_SIZE):
            for y in range(x + 1, TILE_SET_SIZE + 1):
                for z in range(4):
                        # Match tiles which are not edges
                        if ((CreateTile.tileList[x][z] == CreateTile.tileList[y][0]) and (CreateTile.tileList[y][0] != 0)):
                            print(f"tile {x} matches tile {y} on side {z} with edge {CreateTile.tileList[x][z]}")

    def rotateTile(x):
        temp = CreateTile.tileList[x][0]
        CreateTile.tileList[x][0] = CreateTile.tileList[x][3]
        CreateTile.tileList[x][3] = CreateTile.tileList[x][2]
        CreateTile.tileList[x][2] = CreateTile.tileList[x][1]
        CreateTile.tileList[x][1] = temp

    def rotatePosition(x, position):
        temp = position[x][0]
        position[x][0] = position[x][3]
        position[x][3] = position[x][2]
        position[x][2] = position[x][1]
        position[x][1] = temp

    #New for file version
    def rotatePosition(position):
        temp = position[0]
        position[0] = position[3]
        position[3] = position[2]
        position[2] = position[1]
        position[1] = temp
        return position

    def swapPosition(x):
        temp = CreateTile.tileList[x][0]
        CreateTile.tileList[x][0] = CreateTile.tileList[x][1]
        CreateTile.tileList[x][1] = temp