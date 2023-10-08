import cv2
import numpy as np
import pylab
from typing import Union, List

def detector(image) -> Union[int, List[float]]:

    # Apply thresholding to segment the image
    _, thresh = cv2.threshold(image, 50, 255, cv2.THRESH_OTSU)

    thresh = cv2.medianBlur(thresh, 3)

    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((1, 1), dtype=int))

    # Apply median filtering to remove noise
    median = cv2.medianBlur(thresh, 5)

    maxValue = 255
    adaptiveMethod = cv2.ADAPTIVE_THRESH_GAUSSIAN_C#cv2.ADAPTIVE_THRESH_MEAN_C #cv2.ADAPTIVE_THRESH_GAUSSIAN_C
    thresholdType = cv2.THRESH_BINARY#cv2.THRESH_BINARY #cv2.THRESH_BINARY_INV
    blockSize = 5 #odd number like 3,5,7,9,11
    C = -3 # constant to be subtracted
    edges = cv2.adaptiveThreshold(median, maxValue, adaptiveMethod, thresholdType, blockSize, C)

    # Find contours and store their coordinates and sizes in arrays
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    particle_coords = []
    particle_sizes = []
    for contour in contours:
        # Compute the center of the contour using moments
        moments = cv2.moments(contour)
        if moments['m00'] != 0:
            cx = int(moments['m10'] / moments['m00'])
            cy = int(moments['m01'] / moments['m00'])
            # Add the center coordinates to the array
            if [cx, cy] not in particle_coords:
                particle_coords.append((cx, cy))
                # Compute the approximate size of the particle using its area
                area = cv2.contourArea(contour)
                size = np.sqrt(area / np.pi)
                # Add the size to the array
                particle_sizes.append(size)

    # Print the coordinates and sizes of the detected particles
    print(particle_coords)
    print(particle_sizes)
    
    return particle_coords, particle_sizes