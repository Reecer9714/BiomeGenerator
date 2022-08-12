import random
from typing import Union
import numpy as np
from multiprocessing import Pool, shared_memory
from PIL import Image
from noise import snoise2
from intervaltree import IntervalTree, Interval

from config import config
from window import MainWindow
from util import *

RED = TEMP = 0
GREEN = ELEV = 1
BLUE = HUMID = 2

def noise(nx, ny, seed):
    noise_value = snoise2(nx / config.scale_x, ny / config.scale_y, \
        octaves=config.octaves, persistence=config.persistence, lacunarity=config.lacunarity, \
        base=seed, repeatx=config.image_width, repeaty=config.image_height)
    return int(remap(-1,1,0,255,noise_value))

def generate(callback):
    image_array = np.ndarray((config.image_height, config.image_width, 3), dtype=np.uint8)
    
    parent_shm = shared_memory.SharedMemory(name="NoiseBuffer")
    rng = np.ndarray((3,), buffer=parent_shm.buf)
    rng[0] = random.random()
    rng[1] = random.random()
    rng[2] = random.random()

    arglist = [(y, image_array[y]) for y in range(config.image_height)]

    multiple_results = executor.starmap(thread_task, arglist, 1)

    new_image = Image.fromarray(np.array(multiple_results), mode="RGB")
    callback(new_image)
    return new_image

def thread_task(y: int, image_row):
    parent_shm = shared_memory.SharedMemory(name="NoiseBuffer")
    rng = np.ndarray((3,), buffer=parent_shm.buf)
    for x in range(config.image_width):
        image_row[x] = generatePixel(x, y, image_row[x], rng)
    parent_shm.close()
    del rng
    return image_row

def generatePixel(x: int, y: int, pixel: tuple, rng) -> tuple[float, float, float]:
    pixel[TEMP] = noise(x, y, rng[TEMP]) * 255
    pixel[ELEV] = noise(x, y, rng[ELEV]) * 255
    pixel[HUMID] = noise(x, y, rng[HUMID]) * 255

    distx = abs(x/config.image_width - 0.5)
    disty = abs(y/config.image_height - 0.5)
    dist = distx*distx + disty*disty
    #Vertical Mask Temperature
    pixel[TEMP] -= min(disty*200, pixel[TEMP])
    #Circle Mask Elevation
    pixel[ELEV] -= min(dist*320, pixel[ELEV])
    
    # colorize
    elev_interval: Interval = config.palleteLookup.at( pixel[ELEV] ).pop()
    color: Union[tuple , IntervalTree] = elev_interval.data
    if isinstance(color, IntervalTree):
        color = color.at( pixel[TEMP] ).pop().data
        if isinstance(color, IntervalTree):
            color = color.at( pixel[HUMID] ).pop().data

    biome_color = config.biomeColorMap.get(color, (255, 0, 255))
    # modify brightness slightly based on elevation
    brightness_mod = inv_lerp(elev_interval.begin, elev_interval.end, pixel[ELEV])
    interval_range = clamp((elev_interval.end - elev_interval.begin) / 50, 0, 0.5)
    color_mod = 1 + round((brightness_mod - 0.5) * (0.1 + interval_range), 1)
    bighter_color = tuple(clamp(pixel * color_mod, 0, 255) for pixel in biome_color)
    return bighter_color

def main():
    gui = MainWindow(generate)
    gui.run()

if __name__ == "__main__":
    executor = Pool()

    rng = np.array([random.random(), random.random(), random.random()])
    shm = shared_memory.SharedMemory(create=True, size=rng.nbytes, name="NoiseBuffer")
    shared_rng = np.ndarray(rng.shape, dtype=rng.dtype, buffer=shm.buf)
    shared_rng[:] = rng[:]
    del rng

    main()