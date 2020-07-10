import cv2
import numpy as np
#returns image as a multi dimensional numpy array containing relative intensity of pixels
image=cv2.imread('test_image.jpg')
# first argument is the window where we want to display image, and the second is the image
# STEP 1- CONVERT IMAGE TO GRAY SCALE
lane_image=np.copy(image)
gray=cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)
cv2.imshow('result',gray)
# displays image for infinite time
cv2.waitKey(0)
