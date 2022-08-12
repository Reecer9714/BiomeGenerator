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
    "Flower Forest": (45, 142, 73),
    "Forest": (5, 102, 33),
    "ForestHills": (34, 85, 28),
    "FrozenOcean": (144, 144, 160),
    "FrozenRiver": (160, 160, 255),
    "Hell": (255, 0, 0),
    "Ice Mountains": (160, 160, 160),
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

    beachMap = [
        (0,   60,  "Cold Beach"),
        (60,  100, "Stone Beach"),
        (100, 256, "Beach")
    ]
    beachPallete = IntervalTree.from_tuples(beachMap)

    tempZoneCold = [
        (0,   80,  "Ice Plains"),
        (80, 256, "Cold Taiga")
    ]
    coldPallete = IntervalTree.from_tuples(tempZoneCold)

    tempZoneCool = [
        (0,   100, "Taiga"),
        (100, 256, "Mega Taiga")
    ]
    coolPallete = IntervalTree.from_tuples(tempZoneCool)

    tempZoneModerate = [
        (0,   60,  "Plains"),
        (60,  100, "Forest"),
        (100, 150, "Roofed Forest"),
        (150, 256, "Swampland")
    ]
    moderatePallete = IntervalTree.from_tuples(tempZoneModerate)

    tempZoneWarm = [
        (0,    60, "Desert M"),
        (60,   80, "Mesa"),
        (80,  120, "Savanna"),
        (120, 256, "Jungle")
    ]
    warmPallete = IntervalTree.from_tuples(tempZoneWarm)

    tempZoneHot = [
        (60,  100, "Desert"),
        (100, 256, "Savanna")
    ]
    hotPallete = IntervalTree.from_tuples(tempZoneHot)

    landMap = [
        (0,   60,  coldPallete),
        (60,  80, coolPallete),
        (80,  120, moderatePallete),
        (120,  180, warmPallete),
        (180, 256, hotPallete)
    ]
    landPallete = IntervalTree.from_tuples(landMap)

    mountainMap = [
        (0,  100, "Extreme Hills"),
        (100, 256, "Extreme Hills+")
    ]
    mountainPallete = IntervalTree.from_tuples(mountainMap)

    heightMap = [
        # (0,   50,  "Deep Ocean"), #Deep Ocean
        (0,  100, "Ocean"), #Ocean
        (100, 105, beachPallete),
        (105, 150, landPallete),
        (150, 230, "Extreme Hills Edge"), #Mountain Edge
        (230, 256, "Extreme Hills")
    ]

    palleteLookup = IntervalTree.from_tuples(heightMap)