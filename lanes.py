import cv2
import numpy as np
#returns image as a multi dimensional numpy array containing relative intensity of pixels
image=cv2.imread('test_image.jpg')
# first argument is the window where we want to display image, and the second is the image
# STEP 1- CONVERT IMAGE TO GRAY SCALE
lane_image=np.copy(image)
gray=cv2.cvtColor(lane_image, cv2.COLOR_RGB2GRAY)
# STEP 2- REDUCE NOISE AND SMOOTHEN IMAGE
#uisng a kernel filter of 5*5 with 0 deviation
blur =cv2.GaussianBlur(gray,(5,5),0)
# STEP 3-GRADIENT IMAGE FOR EDGE DETECTION, by using a lower threshold as 50 and higher threshold as 150(ratio=3)
#pixels with gradient below lower threshold are rejected, tjose with gradient greater than upper threshold are accepted and marked as edge,
#and the pixels with gradient between the lower and upper threshold are accepted as edge only if they are connected to a pixel with threshold above upper threshold
canny=cv2.Canny(blur,50,150)
cv2.imshow('result',canny)
# displays image for infinite time
cv2.waitKey(0)
