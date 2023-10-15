import easyocr
import re
import numpy as np
from typing import Tuple

file_scale_path = "scales.csv"


def parse(image: np.ndarray, image_name: str) -> Tuple[int, str]:
    reader = easyocr.Reader(['en'])

    config = ('-l eng --oem 1 --psm 3')
    result = reader.readtext(image, detail=0, paragraph=True)

    reslist = str(result).split(":")
    p = '[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'

    for i in range(len(reslist)):
        if (reslist[i].find("field") != -1):
            t = reslist[i+1]
            num = float(re.findall(p, t)[0])
            tt = t.split()[1][:2]
            if tt.find("u") != -1:
                resolution = num
            else:
                resolution = (num*1000)

            save(image_name, resolution)

            return resolution, 'um'


def save(image_name: str, resolution: int) -> None:
    try:
        data = np.genfromtxt(file_scale_path, delimiter=',', dtype=str)
    except FileNotFoundError:
        data = np.array([]).reshape(0, 2)

    new_data = np.array([image_name, str(resolution)])
    data = np.vstack((data, new_data))

    np.savetxt(file_scale_path, data, delimiter=',', fmt='%s')


def load(image_name: str) -> int:
    try:
        data = np.genfromtxt(file_scale_path, delimiter=',', dtype=str)
    except FileNotFoundError:
        return None

    row = np.where(data[:, 0] == image_name)

    if len(row) > 0:
        resolution = int(data[row][0][1])
        return resolution, 'um'
    else:
        return None
