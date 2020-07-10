import cv2
import numpy as np
import matplotlib.pyplot as plt

def make_coordinates(image,line_parameters):
    #slope and intercept of left or right side
    slope,intercept=line_parameters
    y1=image.shape[0]
    #3/5 has been chosen since we want our 3/5th row highlighted(under consideration) at the moment(specifies the other end of road, one bein the bottom most point i.e. close the view)
    y2=int(y1*(3/5))
    x1=int((y1-intercept)/slope)
    x2=int((y2-intercept)/slope)
    #an array containing the single left or right line coordinates
    return np.array([x1,y1,x2,y2])

# this function return an array of 2 lines: 1 for the left side of road and the other for the right side of the road
def average_slope_intercept(image,lines):
    left_fit=[]
    right_fit=[]

    for line in lines:
        x1,y1,x2,y2=line.reshape(4)
        #the function polyfit here fits a polynomial with degree one that passes through points (x1,y1) and (x2,y2)
        #the third argument is the degree of polynomial, the return value is a tuple containing the slope and intercept of the polynomial
        parameters=np.polyfit((x1,x2),(y1,y2),1)

        slope=parameters[0]
        intercept=parameters[1]
        #for left road as y coordinate(starts from bottom) decrease x increases resulting in a negative slop(see image for clarity)
        if slope<0:
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))

#we average out the slopes(axis=0) of all lines on left side and right side and create a new single line for both sides
    left_fit_average=np.average(left_fit,axis=0)
    right_fit_average=np.average(right_fit,axis=0)
    left_line=make_coordinates(image,left_fit_average)
    right_line=make_coordinates(image,right_fit_average)
    return np.array([left_line,right_line])


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
'''
#returns image as a multi dimensional numpy array containing relative intensity of pixels
image=cv2.imread('test_image.jpg')

# STEP 1- CONVERT IMAGE TO GRAY SCALE
#precison of 2 pixels and 2 degree
lane_image=np.copy(image)
canny_image=canny(lane_image)
cropped_image=region_of_interest(canny_image)
#STEP 4- IDENTIFYING LINES IN THE image
# we use hough tranformation to iddntify lines in the image:
#for each point we plot the rho and theta(radians) for every possible line passing through each point
#where rho=xsin(theta)+ysin(theta), we do this for all points, the plot for each point is a sin eave like structure
# considering the plot between rho and theta as a grid(with bins=each grid), we find no: of lines(from all possible(rho theta combo) lines for all points in the image) inersecting in each bin
#the bin or grid with the no: of intersection lines above a threshold is selected as the final rho and theta value for a straight line
#the below line of code return arrays of such suitable lines from cropped image with rho threshold as 2pixels and theta threshold as 1 degree
#minLineLength=40 means the min accepted line length and maxLineGap=5 implies line with distance between them less than 5 must be clubbed together as a single line
lines=cv2.HoughLinesP(cropped_image,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)
#the below function returns the averaged lines s.t instead of broken lines now, we will have a single left and right line
averaged_lines=average_slope_intercept(lane_image,lines)
#display_lines  function returns all above lines on a masked image of same size as original image
line_image=display_lines(lane_image,averaged_lines)
#combo image is the image formed by doing weighted addition of lane_image(the original colored image) and the line_image(containing straight lines)
#here lane_image has 20%less weight than line_image which is done to make lane_image look darker in comparison to line_image
combo_image=cv2.addWeighted(lane_image,0.8,line_image,1,1)
cv2.imshow('result',combo_image)
# displays image for infinite time
cv2.waitKey(0)
'''


cap=cv2.VideoCapture('test2.mp4')
while(cap.isOpened()):
    _,frame=cap.read()
    canny_image=canny(frame)
    cropped_image=region_of_interest(canny_image)
    #STEP 4- IDENTIFYING LINES IN THE image
    # we use hough tranformation to iddntify lines in the image:
    #for each point we plot the rho and theta(radians) for every possible line passing through each point
    #where rho=xsin(theta)+ysin(theta), we do this for all points, the plot for each point is a sin eave like structure
    # considering the plot between rho and theta as a grid(with bins=each grid), we find no: of lines(from all possible(rho theta combo) lines for all points in the image) inersecting in each bin
    #the bin or grid with the no: of intersection lines above a threshold is selected as the final rho and theta value for a straight line
    #the below line of code return arrays of such suitable lines from cropped image with rho threshold as 2pixels and theta threshold as 1 degree
    #minLineLength=40 means the min accepted line length and maxLineGap=5 implies line with distance between them less than 5 must be clubbed together as a single line
    lines=cv2.HoughLinesP(cropped_image,2,np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)
    #the below function returns the averaged lines s.t instead of broken lines now, we will have a single left and right line
    averaged_lines=average_slope_intercept(frame,lines)
    #display_lines  function returns all above lines on a masked image of same size as original image
    line_image=display_lines(frame,averaged_lines)
    #combo image is the image formed by doing weighted addition of lane_image(the original colored image) and the line_image(containing straight lines)
    #here lane_image has 20%less weight than line_image which is done to make lane_image look darker in comparison to line_image
    combo_image=cv2.addWeighted(frame,0.8,line_image,1,1)
    cv2.imshow('result',combo_image)
    # displays image for infinite time
    cv2.waitKey(1)
