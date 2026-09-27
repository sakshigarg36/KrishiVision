import numpy as np

from preprocessing.satellite import validate_bands


def compute_ndvi(red, near_infrared):
    red, near_infrared = validate_bands(np.asarray(red), np.asarray(near_infrared))
    denominator = near_infrared + red
    return np.divide(near_infrared - red, denominator, out=np.zeros_like(denominator, dtype=float), where=denominator != 0)
