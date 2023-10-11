import os
import sys
import numpy as np
# import matplotlib.pyplot as plt
import cv2 as cv
# import pylab
from model.parse_scale import parser
from model.kmeans import kmeans
from model.common import detector
from model.util import *


# Пока что работает складно, если только грузить изображение в папку с проектом!
# Изображения, сгенерированные YOLO, можно посмотреть по адресу runs/detect/*
# Использование - имя файла и номер модели (см ниже)
# C помощью YOLO возможно расчитывать размеры по Х и У одновременно
# Пример использования:
# python detect_particles.py 1.png 0

def yolo_detect(image_path, size):
    os.system("python yolov7/detect.py --weights yolov7/runs/train/yolov7-tiny-custom3/weights/best.pt --save-txt --no-trace --img-size " +
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


def main() -> int:
    # load image path
    # image_path = sys.argv[1]
    image_path = os.path.join('data_resized', "image_9.png")
    print(image_path)
    # choose type of detection
    # 0 - YOLO
    # 1 - kmeans
    # 2 - common CV
    # if len(sys.argv) > 2:
    #     detector_type = int(sys.argv[2])
    # else:
    #     # default - YOLO
    #     detector_type = 0

    detector_type = 0
    # load image
    image = cv2.imread(image_path)
    copy_image = image.copy()
    # get it in gray shades
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.resize(image, (640, 640), interpolation=cv2.INTER_AREA)

    height, width = image.shape
    # divide picture in 2 parts (photo and info)
    # info = image[width:height, 0:width]
    # image = image[0:width, 0:width]

    # run YOLO
    coordinates, sizes = yolo_detect(image_path, width)
    # sizes = np.array(sizes)
    # sizes = np.sqrt(sizes / np.pi) # это не успели доработать просто

    # coordinates = np.array(coordinates)
    # run parsing of scale
    # scale, units = parser(info)
    # sizes = sizes * (scale / width)

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
    np.savetxt(image_path[:-4] + '_sizes.csv', sizes, delimiter=',')
    np.savetxt(image_path[:-4] + '_coordinates.csv',
               coordinates, delimiter=',')

    return 0

# image path as one argument
if __name__ == '__main__':
    #Rename(os.path.join(os.getcwd(), "images"))
    main()
