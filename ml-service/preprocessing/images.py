def validate_image(image):
    if image is None or getattr(image, "size", 0) == 0:
        raise ValueError("Image input is empty")
    return image
