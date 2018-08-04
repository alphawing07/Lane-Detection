import numpy as np 
import cv2
import math
from drawline import drawline
from drawline2 import drawline2

def grayscale(img):
	return cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)

def canny(img, low_threshold ,high_threshold):
	return cv2.Canny(img, low_threshold, high_threshold)

def gaussian(img, kernel_size):
	return cv2.GaussianBlur(img,(kernel_size,kernel_size),0)

def roi(img,vertices):
	mask = np.zeros_like(img)

	if len(img.shape)>2:
		channel_count = img.shape[2]
		ignore_mask_color = (255,)*channel_count
	else:
		ignore_mask_color = 255

	cv2.fillPoly(mask, vertices, ignore_mask_color)

	masked_image = cv2.bitwise_and(img,mask)
	return masked_image

def hough(img,rho,theta,threshold,min_line_length,max_line_gap):
	lines = cv2.HoughLinesP(img,rho,theta,threshold,np.array([]),min_line_length,max_line_gap)
	# line_img = np.zeros(img.shape,stype =npp.uint8) 1 chanel image grayscale
	line_img = np.zeros((*img.shape, 3), dtype = np.uint8)#3chanle rgb image
	drawline(line_img, lines)
	return line_img

def weighted_img(img,initial_img,a=0.8, b=1., c=0.):
	return cv2.addWeighted(initial_img, a, img, b, c)
"""
    `img` is the output of the hough_lines(), An image with lines drawn on it.
    Should be a blank image (all black) with lines drawn on it.
    
    `initial_img` should be the image before any processing.
    
    The result image is computed as follows:
    
    initial_img * a + img * b + c
    NOTE: initial_img and img must be the same shape!
    """

def filter_colors(image):
	# filter image to contain only white or yellow pixels

	#filter white
	white_threshold = 200
	lower_white = np.array([white_threshold,white_threshold,white_threshold])
	upper_white = np.array([255,255,255])
	white_mask = cv2.inRange(image,lower_white,upper_white)
	white_image = cv2.bitwise_and(image,image,mask = white_mask)

	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	lower_yellow = np.array([90,100,100])
	upper_yellow = np.array([110,255,255])
	yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
	yellow_image = cv2.bitwise_and(image, image, mask=yellow_mask)

	#combining the above images

	image2 = cv2.addWeighted(white_image,1., yellow_image,1.,0.)

	return image2



