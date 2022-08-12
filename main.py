import random
import numpy as np
from multiprocessing import Pool, shared_memory
from PIL import Image
from noise import snoise2
from intervaltree import IntervalTree

from config import config
from window import MainWindow

RED = 0
GREEN = 1
BLUE = 2

def lerp(a: float, b: float, t: float) -> float:
    return (1 - t) * a + t * b

def inv_lerp(a: float, b: float, v: float) -> float:
    return (v - a) / (b - a)

def remap(i_min: float, i_max: float, o_min: float, o_max: float, v: float) -> float:
    return lerp(o_min, o_max, inv_lerp(i_min, i_max, v))

def clamp(n, small, large):
    return max(small, min(n, large))

def noise(nx, ny, seed):
    # Rescale from -1.0:+1.0 to 0:255
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

    arglist = []
    for y in range(config.image_height):
        arglist.append((y, image_array[y]))

    multiple_results = executor.starmap(thread_task, arglist, 1)

    new_image = Image.fromarray(np.array(multiple_results), mode="RGB")
    callback(new_image)
    return new_image

def thread_task(y, image_row):
    parent_shm = shared_memory.SharedMemory(name="NoiseBuffer")
    rng = np.ndarray((3,), buffer=parent_shm.buf)
    for x in range(config.image_width):
        image_row[x] = generatePixel(x, y, image_row[x], rng)
    parent_shm.close()
    del rng
    return image_row

def generatePixel(x, y, pixel, rng):
    pixel[RED] = noise(x, y, rng[RED]) * 255
    pixel[GREEN] = noise(x, y, rng[GREEN]) * 255
    pixel[BLUE] = noise(x, y, rng[BLUE]) * 255

    distx = abs(x/config.image_width - 0.5)
    disty = abs(y/config.image_height - 0.5)
    dist = distx*distx + disty*disty
    pixel[RED] -= min(disty*200, pixel[RED])
    pixel[GREEN] -= min(dist*320, pixel[GREEN])
    
    # colorize
    elev_interval = config.palleteLookup.at( pixel[GREEN] ).pop()
    color = elev_interval.data
    if isinstance(color, IntervalTree):
        color = color.at( pixel[RED] ).pop().data
        if isinstance(color, IntervalTree):
            color = color.at( pixel[BLUE] ).pop().data

    biome_color = config.biomeColorMap.get(color, (255, 0, 255))
    # modify brightness slightly based on elevation
    brightness_mod = inv_lerp(elev_interval.begin, elev_interval.end, pixel[GREEN])
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