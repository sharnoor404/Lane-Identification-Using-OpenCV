import cv2
import numpy as np
import matplotlib.pyplot as plt

def canny(image):
    gray=cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # STEP 2- REDUCE NOISE AND SMOOTHEN IMAGE

    #uisng a kernel filter of 5*5 with 0 deviation
    blur =cv2.GaussianBlur(gray,(5,5),0)

    # STEP 3-GRADIENT IMAGE FOR EDGE DETECTION

    #finds derivative of image so as to identify areas in image where pixel intensity changes rapidly by using a lower threshold as 50 and higher threshold as 150(ratio=3)
    #pixels with gradient below lower threshold are rejected, tjose with gradient greater than upper threshold are accepted and marked as edge,
    #and the pixels with gradient between the lower and upper threshold are accepted as edge only if they are connected to a pixel with threshold above upper threshold
    canny=cv2.Canny(blur,50,150)
    return canny

def region_of_interest(image):
    height=image.shape[0]
    #here we have created an array of polygons since fillPoly accepts multiple polygons rather than a single one
    polygons=np.array([
    [(200,height),(1100,height),(550,250)]
    ])
    #creates an a black image with the same dimensions as image
    mask=np.zeros_like(image)
    #we will be filling the polygon area with white color
    cv2.fillPoly(mask,polygons,255)
    return mask

#returns image as a multi dimensional numpy array containing relative intensity of pixels
image=cv2.imread('test_image.jpg')

# STEP 1- CONVERT IMAGE TO GRAY SCALE

lane_image=np.copy(image)
canny=canny(lane_image)
cv2.imshow('result',region_of_interest(canny))
# displays image for infinite time
cv2.waitKey(0)
