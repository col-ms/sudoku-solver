# script that will take an image containing a sudoku puzzle and
# extract the puzzle to an array representation

import operator
import cv2
import numpy as np
from skimage import measure

# iamge preprocessing function
def pre_process_img(image, skip_dilate: bool=True):
    """
    Uses a Guassian Blurring function, adaptive thresholding, and dilating
    to expose the main features of an image (puzzle in this case)
    """

    # applying the blur
    proc = cv2.GaussianBlur(image.copy(), (9, 9), 0)

    # adaptive threshold using 11 nearest neighbor pixels
    proc = cv2.adaptiveThreshold(
        proc, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )

    # inverting colors to gridlines have non-zero pixel values
    proc = cv2.bitwise_not(proc)

    if not skip_dilate:
        # dilate the image to increase the size of the grid lines
        kernel = np.array(
            [[0.0, 1.0, 0.0], [1.0, 1.0, 1.0], [0.0, 1.0, 0.0]], np.uint8
        )
        proc = cv2.dilate(proc, kernel)

    return proc

def find_puzzle_bounds(image):
    """
    Finds the 4 extreme corners of the largest contour in the image (the puzzle)
    """

    # find contours
    contours, h = cv2.findContours(
        image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # sort by area, descending
    contours = sorted(
        contours, key = cv2.contourArea, reverse = True
    )
    polygon = contours[0] # largest image

    bottom_right, _ = max(
        enumerate([pt[0][0] + pt[0][1] for pt in polygon]),
        key = operator.itemgetter(1)
    )
    top_left, _ = min(
        enumerate([pt[0][0] + pt[0][1] for pt in polygon]),
        key = operator.itemgetter(1),
    )
    bottom_left, _ = min(
        enumerate([pt[0][0] - pt[0][1] for pt in polygon]),
        key = operator.itemgetter(1),
    )
    top_right, _ = max(
        enumerate([pt[0][0] - pt[0][1] for pt in polygon]),
        key = operator.itemgetter(1),
    )

    # return array of all 4 points using indices
    return [
        polygon[top_left][0],
        polygon[top_right][0],
        polygon[bottom_right][0],
        polygon[bottom_left][0]
    ]

def crop_and_warp(image, crop_rect):
    """
    Crops and warps a rectangular section from an image into a similarly
    sized square
    """
    top_left, top_right, bottom_right, bottom_left = (
        crop_rect[0],
        crop_rect[1],
        crop_rect[2],
        crop_rect[3]
    )

    src = np.array(
        [top_left, top_right, bottom_right, bottom_left], dtype = "float32"
    )

    def distance_between(x, y):
        return np.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

    # get longest side in the rectangle
    side = max(
        [
            distance_between(bottom_right, top_right),
            distance_between(top_left, bottom_left),
            distance_between(bottom_right, bottom_left),
            distance_between(top_left, top_right)
        ]
    )

    dst = np.array(
        [[0,0], [side - 1, 0], [side - 1, side - 1], [0, side - 1]],
        dtype = "float32"
    )

    # gets the transformation matrix