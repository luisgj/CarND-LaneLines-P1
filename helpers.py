import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2

def grayscale(img):
    """Applies the Grayscale transform
    This will return an image with only one color channel
    but NOTE: to see the returned image as grayscale
    (assuming your grayscaled image is called 'gray')
    you should call plt.imshow(gray, cmap='gray')"""
    return cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    # Or use BGR2GRAY if you read an image with cv2.imread()
    # return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
def canny(img, low_threshold, high_threshold):
    """Applies the Canny transform"""
    return cv2.Canny(img, low_threshold, high_threshold)

def gaussian_blur(img, kernel_size):
    """Applies a Gaussian Noise kernel"""
    return cv2.GaussianBlur(img, (kernel_size, kernel_size), 0)

def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    `vertices` should be a numpy array of integer points.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)   
    
    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    #filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


def draw_lines(img, lines, color=[255, 0, 0], thickness=10):
    """
    Enhanced draw_lines function. 
    Investigated a few implementations on "line extrapolation"
    this function is a version of the implementation of the research on this feature.
    """     
    ymin_global = img.shape[0]
    ymax_global = img.shape[0]
    
    left_slope = []
    left_y = []
    left_x = []
    
    right_slope = []
    right_y = []
    right_x = []
    
    for line in lines:
        for x1,y1,x2,y2 in line:
            # apparently getting the slope and "b" value is easy with numpy
            slope, _ = np.polyfit((x1,x2),(y1,y2),1)
            ymin_global = min(min(y1, y2),ymin_global)
            
            # positive slopes are the left lane lines and viceversa
            if (slope > 0):
                left_slope += [slope]
                left_y += [y1, y2]
                left_x += [x1, x2]
            else:
                right_slope += [slope]
                right_y += [y1, y2]
                right_x += [x1, x2]
                
    # It seems that in the second video some images don't detect lines
    # for some reason :( this statement fixes that particular issue by
    # validating that there are valid lines detected.
    if(len(right_slope) > 0 and len(left_slope) > 0):
        # So based on this question
        # I must take the mean value for all the parameters and values
        # m, x, y and b for each lane side.
        # https://knowledge.udacity.com/questions/636869
        left_mean_slope = np.mean(left_slope, axis=0)
        left_y_mean = np.mean(left_y, axis=0)
        left_x_mean = np.mean(left_x, axis=0)
        # b = y - mx
        left_intercept = left_y_mean - (left_mean_slope * left_x_mean)

        right_mean_slope = np.mean(right_slope, axis=0)
        right_y_mean = np.mean(right_y, axis=0)
        right_x_mean = np.mean(right_x, axis=0)
        # b = y - mx
        right_intercept = right_y_mean - (right_mean_slope * right_x_mean)

        # if    y = mx + b, 
        # then  x = (y - b)/m
        top_left_x = int((ymin_global - left_intercept) / left_mean_slope)
        bottom_left_x = int((ymax_global - left_intercept) / left_mean_slope)
        top_right_x = int((ymin_global - right_intercept) / right_mean_slope)
        bottom_right_x = int((ymax_global - right_intercept) / right_mean_slope)

        cv2.line(
            img,
            (top_left_x, ymin_global), 
            (bottom_left_x, ymax_global),
            color,
            thickness
        )
        cv2.line(
            img,
            (top_right_x, ymin_global), 
            (bottom_right_x, ymax_global),
            color, 
            thickness
        )
    
def hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    """
    `img` should be the output of a Canny transform.
        
    Returns an image with hough lines drawn.
    """
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    draw_lines(line_img, lines)
    return line_img

# Python 3 has support for cool math symbols.

def weighted_img(img, initial_img, α=0.8, β=1., γ=0.):
    """
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.
    
    `initial_img` should be the image before any processing.
    
    The result image is computed as follows:
    
    initial_img * α + img * β + γ
    NOTE: initial_img and img must be the same shape!
    """
    return cv2.addWeighted(initial_img, α, img, β, γ)