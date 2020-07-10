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

def display_lines(image,lines):
    #to generate a mask of same size as image
    line_image=np.zeros_like(image)
    #i.e loop only if lines array is not NULL
    if lines is not None:
        for line in lines:
            #since line is a 1*4 array we break it into segments
            x1,y1,x2,y2=line.reshape(4)
            #the below code is used to add lines to the image line_image with color blue and line weight as 10
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)
    return line_image

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
    masked_image=cv2.bitwise_and(image,mask)
    return masked_image

#returns image as a multi dimensional numpy array containing relative intensity of pixels
image=cv2.imread('test_image.jpg')

# STEP 1- CONVERT IMAGE TO GRAY SCALE
#precison of 2 pixels and 2 degree
lane_image=np.copy(image)
canny=canny(lane_image)
cropped_image=region_of_interest(canny)
#STEP 4- IDENTIFYING LINES IN THE image
# we use hough tranformation to iddntify lines in the image:
#for each point we plot the rho and theta(radians) for every possible line passing through each point
#where rho=xsin(theta)+ysin(theta), we do this for all points, the plot for each point is a sin eave like structure
# considering the plot between rho and theta as a grid(with bins=each grid), we find no: of lines(from all possible(rho theta combo) lines for all points in the image) inersecting in each bin
#the bin or grid with the no: of intersection lines above a threshold is selected as the final rho and theta value for a straight line
#the below line of code return arrays of such suitable lines from cropped image with rho threshold as 2pixels and theta threshold as 1 degree
#minLineLength=40 means the min accepted line length and maxLineGap=5 implies line with distance between them less than 5 must be clubbed together as a single line
lines=cv2.HoughLinesP(cropped_image,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)
#display_lines  function returns all above lines on a masked image of same size as original image
line_image=display_lines(lane_image,lines)
#combo image is the image formed by doing weighted addition of lane_image(the original colored image) and the line_image(containing straight lines)
#here lane_image has 20%less weight than line_image which is done to make lane_image look darker in comparison to line_image
combo_image=cv2.addWeighted(lane_image,0.8,line_image,1,1)
cv2.imshow('result',combo_image)
# displays image for infinite time
cv2.waitKey(0)
