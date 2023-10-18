import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import cv2 as cv
import model.scaleparse as scale
from typing import Tuple
import detect


weights_path = os.path.join(
    "weights", "yolov7-custom101t", "weights", "best.pt")
project_path = "detected"


def yolo(image_name: str, size: int) -> None:
    image_path = os.path.join("data_resized", image_name)

    detect.main(['--weights', weights_path, '--source', image_path,
                 '--img-size', str(size), '--save-txt', '--no-trace',
                 '--project', project_path, '--name', image_name[:-4], '--class', '0'])


def graph(image_name: str) -> None:
    resolution, units, width = scale.load(image_name)

    sizes = getSizes(loadLabels(image_name), width)
    sizes = sizes * (resolution / width)

    sns.set_theme()
    plt.hist(sizes)
    plt.xlabel("Scale," + units)
    plt.ylabel("Particles count")
    plt.legend(["Distribution of sizes"])


def loadImage(image_name: str, info: np.ndarray) -> Tuple[np.ndarray, int, str]:
    resolution, units, _ = scale.load(image_name)
    path = os.path.join(
        project_path, image_name[:-4], image_name)
    image = cv.imread(path)
    if type(info) == np.ndarray and info.size > 0:
        info = cv.cvtColor(info, cv.COLOR_GRAY2RGB)
        info = cv.resize(info, (640, 75), interpolation=cv.INTER_AREA)
        image = np.vstack([image, info])

    return image, resolution, units


def loadLabels(image_name: str) -> np.ndarray:
    path = os.path.join(
        project_path, image_name[:-4], "labels", image_name[:-3] + 'txt')
    return np.loadtxt(path)


def getSizes(labels: np.ndarray, size: int) -> np.ndarray:
    sizes = []
    for label in labels:
        sizes.append((round(label[3]*size) + round(label[4]*size)) // 2)
    sizes = np.array(sizes)
    sizes = np.sqrt(sizes / np.pi)
    return sizes


def getCoor(labels: np.ndarray, size: int) -> np.ndarray:
    coordinates = []
    for label in labels:
        coordinates.append((round(label[1]*size), round(label[2]*size)))
    return np.array(coordinates)


def run(image: np.ndarray, image_name: str) -> Tuple[np.ndarray, int, str]:
    height, width = image.shape
    info = None

    if scale.load(image_name) != None:
        image, resolution, units = loadImage(
            image_name, image[width:height, 0:width])
        return image, resolution, units

    # divide picture in 2 parts (photo and info)
    if height != width:
        info = image[width:height, 0:width]
        image = image[0:width, 0:width]
        _, _, _ = scale.parse(info, image_name)

    image = cv.resize(image, (640, 640), interpolation=cv.INTER_AREA)
    height, width = image.shape

    image_path = os.path.join("data_resized", image_name)
    cv.imwrite(image_path, image)

    # run YOLO
    yolo(image_name, width)

    image, resolution, units = loadImage(image_name, info)
    return image, resolution, units
