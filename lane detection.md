# Contents
1.Functions used 

2.Constants

3.drawline 

4.Annotate
## Import Modules
```python

  import numpy as np 
  import cv2
  import matplotlib.pyplot as plt
  import matplotlib.image  as mpimg
  from moviepy.editor import VideoFileClip
  ```
## 1. Functions used 
```python

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

def filter_colors(image):
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
  ```
  ## 2. Constants
  ```python
  
	kernel_size = 3

	#canny
	low_threshold = 50
	high_threshold = 150

	#ROI
	trap_bottom_width = 0.85
	trap_top_width = 0.07
	trap_height = 0.4

	#hough
	rho = 1
	theta =1*np.pi/180
	threshold = 14
	min_line_length = 15
	max_line_gap = 20
```
## 3. Drawline function
plot lines using cordinates returned by Hough
```python
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

```
## 4.Annotate
perform necessary processes on the image and superimpose detected lanes on original image 
```python
def annotate(image_in):

	image = filter_colors(image_in)

	gray = grayscale(image)

	blur_gray = gaussian(gray , c1.kernel_size)	

	edges = canny(blur_gray, c1.low_threshold, c1.high_threshold)

	imshape = image.shape


	vertices = np.array([[\
        	((imshape[1] * (1 - c1.trap_bottom_width)) // 2, imshape[0]),\
        	((imshape[1] * (1 - c1.trap_top_width)) // 2, imshape[0] - imshape[0] * c1.trap_height),\
        	(imshape[1] - (imshape[1] * (1 - c1.trap_top_width)) // 2, imshape[0] - imshape[0] * c1.trap_height),\
        	(imshape[1] - (imshape[1] * (1 - c1.trap_bottom_width)) // 2, imshape[0])]]\
       		, dtype=np.int32)

	masked_edges = roi(edges, vertices)

	line_image = hough(masked_edges, c1.rho, c1.theta, c1.threshold, c1.min_line_length, c1.max_line_gap)

	initial_image = image_in.astype('uint8')
	annotated_image = weighted_img(line_image, initial_image)

	return annotated_image

```
## Testing images
 ```python
  
	  image = mpimg.imread('test/solidYellowCurve.jpg')
	  out=annotate(image)
	  mpimg.imsave('out/gray',out)
```
## Testing video clips 
```python
  def processimg(image):
    result = annotate(image)
    return result
    
  output = 'testvideo.mp4'
  clip1 = VideoFileClip("test/testvideo.mp4")
  clip = clip1.fl_image(processimg)
  clip.write_videofile(output,audio= False)
 ```

