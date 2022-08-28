from intervaltree import IntervalTree

class config:
    image_width = 640
    image_height = 640

    scale_x = image_width / 4
    scale_y = image_height / 4
    octaves = 8
    persistence = 0.5
    lacunarity = 2.0

    biomeColorMap = {
    "Beach": (250, 222, 85),
    "Birch Forest Hills M": (31, 80, 46),
    "Birch Forest Hills": (31, 95, 50),
    "Birch Forest M": (78, 110, 88),
    "Birch Forest": (48, 116, 68),
    "Cold Beach": (250, 240, 192),
    "Cold Taiga Hills": (36, 63, 54),
    "Cold Taiga M": (46, 80, 70),
    "Cold Taiga": (49, 85, 74),
    "Deep Ocean": (0, 0, 48),
    "Desert M": (229, 130, 8),
    "Desert": (250, 148, 24),
    "DesertHills": (210, 95, 18),
    "Extreme Hills Edge": (114, 120, 154),
    "Extreme Hills M": (82, 82, 82),
    "Extreme Hills+ M": (70, 98, 70),
    "Extreme Hills+": (80, 112, 80),
    "Extreme Hills": (96, 96, 96),
    "Snowy Mnts": (255, 255, 255),
    "Flower Forest": (45, 142, 73),
    "Forest": (5, 102, 33),
    "ForestHills": (34, 85, 28),
    "FrozenOcean": (144, 144, 160),
    "FrozenRiver": (160, 160, 255),
    "Hell": (255, 0, 0),
    "Ice Mountains": (160, 160, 170),
    "Ice Plains Spikes": (140, 180, 180),
    "Ice Plains": (255, 255, 255),
    "Jungle M": (76, 112, 9),
    "Jungle": (83, 123, 9),
    "JungleEdge M": (90, 128, 21),
    "JungleEdge": (98, 139, 23),
    "JungleHills": (44, 66, 5),
    "Mega Spruce Taiga Hills": (71, 81, 65),
    "Mega Spruce Taiga": (129, 142, 121),
    "Mega Taiga Hills": (69, 79, 62),
    "Mega Taiga": (89, 102, 81),
    "Mesa (Bryce)": (228, 86, 39),
    "Mesa Plateau F M": (166, 143, 95),
    "Mesa Plateau F": (176, 151, 101),
    "Mesa Plateau M": (183, 127, 92),
    "Mesa Plateau": (202, 140, 101),
    "Mesa": (217, 69, 21),
    "MushroomIsland": (255, 0, 255),
    "MushroomIslandShore": (160, 0, 255),
    "Ocean": (0, 0, 112),
    "Plains": (141, 179, 96),
    "River": (0, 0, 255),
    "Roofed Forest M": (54, 68, 22),
    "Roofed Forest": (64, 81, 26),
    "Savanna M": (91, 128, 21),
    "Savanna Plateau M": (153, 144, 92),
    "Savanna Plateau": (167, 157, 100),
    "Savanna": (189, 178, 95),
    "Sky": (128, 128, 255),
    "Stone Beach": (162, 162, 132),
    "Sunflower Plains": (222, 255, 0),
    "Swampland M": (40, 210, 159),
    "Swampland": (7, 249, 178),
    "Taiga M": (10, 91, 79),
    "Taiga": (11, 102, 89),
    "TaigaHills": (22, 57, 51),
    "The Void": (182, 208, 255),
    }

    freezing_point = 30
    sea_level = 100
    tree_line = 150

    #Humidity
    coldPallete = IntervalTree.from_tuples([
        (0,   80,  "Ice Plains"),
        (80, 256, "Cold Taiga")
    ])

    coolPallete = IntervalTree.from_tuples([
        (0,   100, "Taiga"),
        (100, 256, "Mega Taiga")
    ])

    moderatePallete = IntervalTree.from_tuples([
        (0,   60,  "Plains"),
        (60,  100, "Forest"),
        (100, 150, "Roofed Forest"),
        (150, 256, "Swampland")
    ])

    warmPallete = IntervalTree.from_tuples([
        (0,    60, "Desert M"),
        (60,   80, "Mesa"),
        (80,  120, "Savanna"),
        (120, 256, "Jungle")
    ])

    hotPallete = IntervalTree.from_tuples([
        (0,   60,  "Desert"), # Barren?
        (60,  100, "Desert"),
        (100, 256, "Savanna")
    ])

    # Temperature
    oceanPallete = IntervalTree.from_tuples([
        (0,   freezing_point/2,  "FrozenOcean"),
        (freezing_point/2,  256, "Ocean")
    ])

    beachPallete = IntervalTree.from_tuples([
        (0,   freezing_point,  "Stone Beach"),
        (freezing_point,  100, "Cold Beach"),
        (100, 256, "Beach")
    ])

    landPallete = IntervalTree.from_tuples([
        (0,   freezing_point,  coldPallete),
        (freezing_point,  80, coolPallete),
        (80,  120, moderatePallete),
        (120,  180, warmPallete),
        (180, 256, hotPallete)
    ])

    mountainPallete = IntervalTree.from_tuples([
        (0,  freezing_point, "Ice Mountains"),
        (freezing_point, 256, "Snowy Mnts")
    ])

    # Elevation
    palleteLookup = IntervalTree.from_tuples([
        # (0,   50,  "Deep Ocean"), #Deep Ocean
        (0,  sea_level, oceanPallete),
        (sea_level, 105, beachPallete),
        (105, tree_line, landPallete),
        (tree_line, tree_line+30, "Extreme Hills"), #Mountain Edge
        (tree_line+30, 256, mountainPallete)
    ])