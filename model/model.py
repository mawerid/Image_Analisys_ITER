import os
import sys
import numpy as np
# import matplotlib.pyplot as plt
import cv2 as cv
# import pylab
from model.scaleparse import parse
from typing import Tuple, List


def detect(image_path, size) -> Tuple[List, List]:
    os.system("python yolov7/detect.py --weights weights/yolov7-tiny_custom_5/weights/best.pt --save-txt --no-trace --img-size " +
              str(size) + " --source " + image_path)
    filename = "runs/detect/exp/labels/" + image_path[-11:-3] + 'txt'

    size_x = []
    size_y = []
    sizes = []
    coordinates = []

    with open(filename) as labels:
        for line in labels:
            lst = line.split()
            lst = [float(x) for x in lst]
            coordinates.append((round(lst[1]*size), round(lst[2]*size)))
            size_x.append(round(lst[3]*size))
            size_y.append(round(lst[4]*size))
            sizes.append((round(lst[3]*size) + round(lst[4]*size)) // 2)

    return (coordinates, sizes)


def graph():
    pass

def loadImage():
    pass

def run() -> int:
    # load image path
    # image_path = sys.argv[1]

    image_path = os.path.join('data_resized', "56-100.png")
    print(image_path)

    # load image
    image = cv.imread(image_path)
    copy_image = image.copy()
    # get it in gray shades
    image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    height, width = image.shape
    # divide picture in 2 parts (photo and info)
    info = image[width:height, 0:width]
    image = image[0:width, 0:width]
    image = cv.resize(image, (640, 640), interpolation=cv.INTER_AREA)
    height, width = image.shape

    # run YOLO
    coordinates, sizes = detect(image_path, width)
    print(sizes)
    sizes = np.array(sizes)
    sizes = np.sqrt(sizes / np.pi)  # это не успели доработать просто

    coordinates = np.array(coordinates)
    # run parsing of scale
    scale, units = parser(info)
    print(scale, units)
    sizes = sizes * (scale / width)

    # Этот код должен выводить гистограмму и картинку, однако у нас отказала библиотека в послений момент
    # Если не работает, то закомментируйте этот код
    # generate gistogramm of masses and save it
    # plt.hist(sizes)
    # plt.xlabel("Scale, " + units)
    # plt.ylabel("Particles count")
    # plt.legend(["Distribution of sizes"])
    # plt.savefig("Distribution.png")

    # И этот тоже
    # Display the resulting image with particle centers marked
    # for i, coords in enumerate(coordinates):
    #     cv2.circle(image, (coords[0], coords[1]), 3, (0, 0, 255), -1)
    #     cv2.putText(image, f"{sizes[i]:.2f}", (coords[0] + 5, coords[1] - 5),
    #                 cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    # pylab.figure(0)
    # pylab.imshow(image)

    # save csv files (without units)
    # np.savetxt(image_path[:-4] + '_sizes.csv', sizes, delimiter=',')
    # np.savetxt(image_path[:-4] + '_coordinates.csv',
    #            coordinates, delimiter=',')

    return 0
