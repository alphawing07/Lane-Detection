import numpy as np 
import cv2
import math
import constants as c1

def  drawline(img,lines, color = [255,0,0], thickness=10):
	draw_right = True
	draw_left = True

	slope_threshold = 0.5
	slopes = []
	new_lines  = []
	for line in lines:
		x1,y1,x2,y2 = line[0]

		if x2-x1 == 0:
			slope = 999.
		else:
			slope = (y2-y1)/(x2-x1)

		if abs(slope)> slope_threshold:
			slopes.append(slope)
			new_lines.append(line)

	lines = new_lines

	right_lines = []
	left_lines = []
	for i,line in enumerate(lines):
		x1,y1,x2,y2 = line[0]
		img_x_center = img.shape[1]/2
		if slopes[i] > 0 and x1 >img_x_center and x2 > img_x_center:
			right_lines.append(line)
		elif slopes[i] < 0 and x1 < img_x_center and x2< img_x_center:
			left_lines.append(line)

	right_lines_x = []
	right_lines_y = []

	for line in right_lines:
		x1,y1,x2,y2 = line[0]
		right_lines_x.append(x1)
		right_lines_x.append(x2)

		right_lines_y.append(y1)
		right_lines_y.append(y2)

	if len(right_lines_x) >0:
		right_m,right_b = np.polyfit(right_lines_x,right_lines_y,1)
	else:
		right_m,right_b =1,1
		draw_right = False

	left_lines_x = []
	left_lines_y = []

	for line in left_lines:
		x1,y1,x2,y2 = line[0]
		left_lines_x.append(x1)
		left_lines_x.append(x2)

		left_lines_y.append(y1)
		left_lines_y.append(y2)

	if len(left_lines_x) >0:
		left_m,left_b = np.polyfit(left_lines_x,left_lines_y,1)
	else:
		left_m,left_b =1,1
		draw_left = False


	y1 = img.shape[0]
	y2 = img.shape[0]*(1-c1.trap_height)

	right_x1 = (y1 - right_b)/right_m
	right_x2 = (y2 - right_b)/right_m

	left_x1 = (y1 - left_b)/left_m
	left_x2 = (y2 - left_b)/left_m

	y1 = int(y1)
	y2 = int(y2)

	right_x1 = int(right_x1)
	right_x2 = int(right_x2)

	left_x1 = int(left_x1)
	left_x2 = int(left_x2)

	if draw_right:
		cv2.line(img,(right_x1,y1),(right_x2,y2),[0,255,0], thickness)

	if draw_left:
		cv2.line(img, (left_x1,y1), (left_x2,y2),[0,255,0], thickness)




