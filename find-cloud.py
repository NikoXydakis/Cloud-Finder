#!/usr/bin/env python
"This program identifies the clouds in the sky. It takes an image \
as an input and locates the clouds in the sky, then it marks the cloud \
with yellow and it displays the original image and the processed one side by side"
from __future__ import division
import sys, cv2, numpy as np, pylab

#----------------
# Functions     |
#----------------

def round_num (x):
    "This function converts a number to its nearest whole\
    number."
    return int (round (x))

#------------------------
# find-cloud.py - START |
#------------------------

" At first we want the user to input a source for the images, \
then we need to check if the user input is correct for our \
program to work"

if len (sys.argv) < 2:
    print >>sys.stderr, "Usage:", sys.argv[0], "<image>..."
    sys.exit (1)

" If the user input is correct we proceed with the file manipulation. \
The actions taken will be applied to every image that the source folder contains."
    
for fn in sys.argv[1:]:
    im = cv2.imread (fn)
    print fn
		
    "Images are defined with the RGB color space. This color space works fine \
    when we need to describe exact color, in this case though the color of a cloud\
    is also affect by shadows, the time of day that the picture was taken as long as\
    the transparency of the cloud. Therefore we need to convert our image to HSV colorspace\
    which is more suitable for object tracking since it's a lot easier to describe color with it."
    
    hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    
    "Once the color space of the image has been converted \
    we need to set HSV color ranges in order to track the colors.\
    First we define the color that we want in our final mask \
    and then the colors that will be removed from the final mask."
    
    # white 
    lower_white = np.array([0, 0, 240])
    upper_white = np.array([255, 15, 255])
    
    # white type 2
    lower_white2 = np.array([43, 19, 19])
    upper_white2 = np.array([63, 234, 234])
    
    # bright white
    lower_bwhite = np.array([22, 18, 18])
    upper_bwhite = np.array([42, 254, 254])
    
    # gray
    lower_gray = np.array([0, 100, 100])
    upper_gray = np.array([20, 255, 255])
    
    # darker gray
    lower_dgray = np.array([74, 8, 8])
    upper_dgray = np.array([94, 12, 12])
    
    # gray type 2
    lower_gray2 = np.array([35, 22, 22])
    upper_gray2 = np.array([55, 139, 139])
    
    # green-ish
    lower_green = np.array([64, 13, 13])
    upper_green = np.array([84, 77, 77])
    
    # colors to be subtracted from the final mask
    
    # blue
    lower_blue = np.array([63, 50, 50])
    upper_blue = np.array([83, 50, 50])
    
    # light blue
    lower_lightblue = np.array([86, 71, 191])
    upper_lightblue = np.array([106, 71, 191])
    
    # light sky
    lower_lightsky = np.array([33, 45, 45])
    upper_lightsky = np.array([53, 210, 210])
    
    # tree
    lower_tree = np.array([22, 24, 24])
    upper_tree = np.array([42, 170, 170])
    
    "Creating all the individual masks according to the colors\
    we specified earlier."
    
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    mask_white2 = cv2.inRange(hsv, lower_white2, upper_white2)
    mask_bwhite = cv2.inRange(hsv, lower_bwhite, upper_bwhite)
    mask_gray = cv2.inRange(hsv, lower_gray, upper_gray)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_gray2 = cv2.inRange(hsv, lower_gray2, upper_gray2)
    mask_dgray = cv2.inRange(hsv, lower_dgray, upper_dgray)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_tree = cv2.inRange(hsv, lower_tree, upper_tree)  
    mask_lightblue = cv2.inRange(hsv, lower_lightblue, upper_lightblue)
    mask_lightsky = cv2.inRange(hsv, lower_lightsky, upper_lightsky)
    
    "All the masks need to be combined into one and then applied \
    to the original image. First the original image is duplicated, \
    the result mask is applied and the clouds color changes to yellow. "
    
    result_mask = (mask_white + mask_white2 + mask_bwhite + 
                   mask_green + mask_gray + mask_gray2 + 
                   mask_dgray - mask_blue - 
                   mask_lightblue - mask_tree - mask_lightsky)
    
    yellow_im = im.copy()
    
    yellow_im[result_mask > 0] = (23, 222, 255)
    
    "After all calculations and changes have been made, we combine the \
    original image and the result image in the same window side by side. \
    The new window will be too large to be shown in smaller screens therefore, \
    we need to change the dimentions according the maximum width that we've set. \
    Finally the result window will be displayed for 2 seconds on the screen."
    
    max_display = 800
    
    result_window = np.concatenate((im, yellow_im), axis=1)
    ny, nx, nc = result_window.shape
    
    if ny > max_display or nx > max_display:
        nmax = max (ny, nx)
        fac = max_display / nmax
        nny = round_num (ny * fac)
        nnx = round_num (nx * fac)
        result_window = cv2.resize (result_window, (nnx, nny)) 
        
    cv2.imshow(fn, result_window)
    cv2.waitKey(2000)
    cv2.destroyWindow(fn)

#-------------------------
# find-cloud.py - FINISH |
#-------------------------