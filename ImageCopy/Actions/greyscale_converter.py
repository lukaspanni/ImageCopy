# pylint: skip-file
"""
Functions for auto greyscale
"""
import numpy as np
from numba import stencil, njit, cuda


@stencil(neighborhood=((0, 0), (0, 0), (0, 2)))
def stencil_avg(px):
    return np.mean(px[0, 0, 0:3])


@stencil(neighborhood=((0, 0), (0, 0), (0, 2)))
def stencil_luminosity(px):
    return px[0, 0, 0] * 0.21 + px[0, 0, 1] * 0.72 + px[0, 0, 2] * 0.07


@stencil(neighborhood=((0, 0), (0, 0), (0, 2)))
def stencil_lightness(px):
    return 0.5 * (np.max(px[0, 0, 0:3]) + np.min(px[0, 0, 0:3]))


@njit(parallel=True)
def greyscale_avg(arr):
    return stencil_avg(arr)


@njit(parallel=True)
def greyscale_luminosity(arr):
    return stencil_luminosity(arr)


@njit(parallel=True)
def greyscale_lightness(arr):
    return stencil_lightness(arr)


@cuda.jit(device=True)
def gpu_avg(px_val):
    return (px_val[0] + px_val[1] + px_val[2]) // 3


@cuda.jit(device=True)
def gpu_luminosity(px_val):
    return (px_val[0] * 0.21 + px_val[1] * 0.72 + px_val[2] * 0.07) // 1


@cuda.jit(device=True)
def gpu_lightness(px_val):
    return (0.5 * (max(px_val[0], px_val[1], px_val[2]) + min(px_val[0], px_val[1], px_val[2]))) // 1


@cuda.jit()
def gpu_greyscale_avg(img):
    x, y = cuda.grid(2)
    d1, d2 = cuda.gridsize(2)
    for i in range(x, img.shape[0], d1):
        for j in range(y, img.shape[1], d2):
            img[i][j] = gpu_avg(img[i][j])


@cuda.jit()
def gpu_greyscale_luminosity(img):
    x, y = cuda.grid(2)
    d1, d2 = cuda.gridsize(2)
    for i in range(x, img.shape[0], d1):
        for j in range(y, img.shape[1], d2):
            img[i][j] = gpu_luminosity(img[i][j])


@cuda.jit()
def gpu_greyscale_lightness(img):
    x, y = cuda.grid(2)
    d1, d2 = cuda.gridsize(2)
    for i in range(x, img.shape[0], d1):
        for j in range(y, img.shape[1], d2):
            img[i][j] = gpu_lightness(img[i][j])


algorithms = {
    "average": {"cpu": greyscale_avg, "gpu": gpu_greyscale_avg},
    "luminosity": {"cpu": greyscale_luminosity, "gpu": gpu_greyscale_luminosity},
    "lightness": {"cpu": greyscale_lightness, "gpu": gpu_greyscale_lightness}
}


class GreyscaleConverter:
    algorithm: str

    def __init__(self):
        self.gpu = cuda.is_available()

    def execute(self, img_data):
        if not self.gpu:
            return algorithms[self.algorithm]["cpu"](img_data).astype(np.uint8)[:, :, 0]
        dev_arr = cuda.to_device(img_data)
        algorithms[self.algorithm]["gpu"][(32, 32), (16, 16)](dev_arr)
        return dev_arr.copy_to_host()
