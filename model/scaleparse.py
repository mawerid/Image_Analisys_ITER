import easyocr
import re
import numpy as np
import os
from typing import Tuple

file_scale_path = os.path.join("meta", "scales.csv")


def parse(image: np.ndarray, image_name: str) -> Tuple[int, str, int]:
    resolution = load(image_name)
    if resolution != None:
        return resolution

    reader = easyocr.Reader(['en'])

    height, width = image.shape
    image = image[0:height, (width//2):width]

    result = reader.readtext(image, detail=0, paragraph=True)

    resolution, units = result[1].split()
    resolution = int(resolution)

    save(image_name, resolution, units, width)

    return resolution, units, width


def save(image_name: str, resolution: int, units: str, width: int) -> None:
    try:
        data = np.genfromtxt(file_scale_path, delimiter=',', dtype=str)
    except FileNotFoundError:
        data = np.array([]).reshape(0, 4)

    new_data = np.array([image_name, str(resolution), units, str(width)])
    data = np.vstack([data, new_data])

    np.savetxt(file_scale_path, data, delimiter=',', fmt='%s')


def load(image_name: str) -> Tuple[int, str, int]:
    try:
        data = np.genfromtxt(file_scale_path, delimiter=',', dtype=str)
    except FileNotFoundError:
        return None

    row = np.where(data[:] == image_name)

    if len(row[0]) > 0:
        resolution = int(data[row[0][0]][1])
        units = data[row[0][0]][2]
        width = int(data[row[0][0]][3])
        return resolution, units, width
    else:
        return None
