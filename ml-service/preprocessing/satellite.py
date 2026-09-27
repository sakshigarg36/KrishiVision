def validate_bands(red, near_infrared):
    if red.shape != near_infrared.shape:
        raise ValueError("Red and near-infrared bands must have the same shape")
    return red, near_infrared
