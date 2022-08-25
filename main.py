from math import cos, sin, tau
from enum import IntEnum
import random
from typing import Callable, Union
import numpy as np
from multiprocessing import Pool, shared_memory
from PIL import Image
from noise import snoise2
from intervaltree import IntervalTree, Interval

from config import config
from util import *

class Channel(IntEnum):
    TEMP = 0
    ELEV = 1
    HUMID = 2

def noise(nx, ny, seed, octives=config.octaves, pers=config.persistence, lac=config.lacunarity) -> float:
    noise_config = {
        "octaves": octives,
        "persistence":pers,
        "lacunarity":lac,
        # "base":seed
    }
    point_2d = (nx/config.scale_x,ny/config.scale_y)
    noise_value = snoise2(*point_2d, **noise_config)
    return remap(-1,1,0,1,noise_value)

def generateSeeds():
    parent_shm = shared_memory.SharedMemory(name="SeedBuffer")
    seeds = np.ndarray((3,), buffer=parent_shm.buf)
    seeds[Channel.TEMP] = random.random()*100
    seeds[Channel.ELEV] = random.random()*100
    seeds[Channel.HUMID] = random.random()*100

def regenerateChannelSeed(channel: Channel):
    parent_shm = shared_memory.SharedMemory(name="SeedBuffer")
    seeds = np.ndarray((3,), buffer=parent_shm.buf)
    seeds[channel] = random.random()*100

def generateImages(callback: Callable[[Image.Image, Image.Image], None]):
    image_array = np.ndarray((config.image_height, config.image_width, 3), dtype=np.uint8)
    
    arglist = [(y, image_array[y]) for y in range(config.image_height)]

    noise_results = executor.starmap(noise_task, arglist, 1)
    biome_results = executor.map(biome_task, noise_results, 1)

    noise_map = Image.fromarray(np.array(noise_results), mode="RGB")
    biome_map = Image.fromarray(np.array(biome_results), mode="RGB")
    callback(noise_map, biome_map)
    return biome_map

def noise_task(y: int, image_row: np.ndarray) -> np.ndarray:
    parent_shm = shared_memory.SharedMemory(name="SeedBuffer")
    seeds = np.ndarray((3,), buffer=parent_shm.buf)
    for x in range(config.image_width):
        image_row[x] = generateNoise(x, y, image_row[x], seeds)
    parent_shm.close()
    del seeds
    return image_row

def generateNoise(x: int, y: int, pixel: tuple, rng) -> tuple[float, float, float]:
    temp_noise = noise(x, y, rng[Channel.TEMP])
    elev_noise = noise(x, y, rng[Channel.ELEV])
    humid_noise = noise(x, y, rng[Channel.HUMID])

    elev_noise = elev_noise ** 1.2

    distx = abs(x/config.image_width - 0.5)
    disty = abs(y/config.image_height - 0.5)
    dist = distx*distx + disty*disty

    masked_temp = max(temp_noise - disty**0.95, 0)
    masked_elev = max(elev_noise - dist**0.95, 0)
    masked_humid = max(humid_noise - (0.05-dist**0.1)*0, 0)

    pixel[Channel.TEMP] = masked_temp * 255
    pixel[Channel.ELEV] = masked_elev * 255
    pixel[Channel.HUMID] = masked_humid * 255
    return pixel

def biome_task(image_row):
    for x in range(config.image_width):
        image_row[x] = generateBiome(image_row[x])
    return image_row

def generateBiome(pixel: tuple) -> tuple[float, float, float]:
    # colorize
    elev_interval: Interval = config.palleteLookup.at( pixel[Channel.ELEV] ).pop()
    color: Union[tuple , IntervalTree] = elev_interval.data
    if isinstance(color, IntervalTree):
        color = color.at( pixel[Channel.TEMP] ).pop().data
        if isinstance(color, IntervalTree):
            color = color.at( pixel[Channel.HUMID] ).pop().data

    biome_color = config.biomeColorMap.get(color, (255, 0, 255))
    # modify brightness slightly based on Channel.elevation
    brightness_mod = inv_lerp(elev_interval.begin, elev_interval.end, pixel[Channel.ELEV])
    interval_range = clamp((elev_interval.end - elev_interval.begin) / 50, 0, 0.5)
    color_mod = 1 + round((brightness_mod - 0.5) * (0.1 + interval_range), 1)
    brighter_color = tuple(clamp(channel * color_mod, 0, 255) for channel in biome_color)
    return brighter_color

def onStartup():
    global executor, shm
    executor = Pool()

    rng = np.array([random.random(), random.random(), random.random()])
    shm = shared_memory.SharedMemory(create=True, size=rng.nbytes, name="SeedBuffer")
    shared_rng = np.ndarray(rng.shape, dtype=rng.dtype, buffer=shm.buf)
    shared_rng[:] = rng[:]
    del rng
    generateSeeds()
