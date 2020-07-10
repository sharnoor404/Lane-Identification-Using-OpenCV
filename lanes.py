import cv2
#returns image as a multi dimensional numpy array containing relative intensity of pixels
image=cv2.imread('test_image.jpg')
#first argument is the window where we want to display image, and the second is the image
cv2.imshow('result',image)
#displays image for infinite time
cv2.waitKey(0)
