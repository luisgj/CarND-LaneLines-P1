import os
import helpers
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# Define the Hough transform parameters
RHO = 1
THETA = np.pi/180
VOTE_NUM = 17
MIN_LINE_LENGTH= 40
MAX_LINE_GAP = 20


def detectLineLanes(image):
    """
    Simple pipeline to detect line lanes.
    Based on the learnings for the first project.
    Using canny edges extractions and hough transforms 
    with provided helper functions.
    """
    gray = helpers.grayscale(image)
    blurred = helpers.gaussian_blur(gray, 5)
    edges = helpers.canny(blurred, 50, 150)
    imshape = image.shape
    roi_vertices = np.array(
        [
            [
                (100,imshape[0]),
                (450, 316),
                (490, 316),
                (imshape[1],imshape[0])
            ]
        ],
        dtype=np.int32
    )
    masked = helpers.region_of_interest(edges, roi_vertices)
    line_image = helpers.hough_lines(
        masked,
        RHO,
        THETA,
        VOTE_NUM,
        MIN_LINE_LENGTH,
        MAX_LINE_GAP
    )
    weighted = helpers.weighted_img(line_image, image)
    return weighted
