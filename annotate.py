from functions import filter_colors,grayscale, gaussian,  canny, roi, hough, weighted_img
import constants as c1
import matplotlib.pyplot as plt
import matplotlib.image  as mpimg
import numpy as np
from moviepy.editor import VideoFileClip

avgLeft = (0, 0, 0, 0)
avgRight = (0, 0, 0, 0)

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

image = mpimg.imread('test/solidYellowCurve.jpg')
out=annotate(image)
mpimg.imsave('out/gray',out)


#def processimg(image):
#	result = annotate(image)
#	return result




#white_output = 'ch.mp4'
#clip1 = VideoFileClip("test/ch.mp4")
#white_clip = clip1.fl_image(processimg)
#white_clip.write_videofile(white_output,audio= False)

#white_output = 'white2.mp4'
#clip1 = VideoFileClip("test/solidWhiteRight.mp4")
#white_clip = clip1.fl_image(processimg)
#white_clip.write_videofile(white_output,audio= False)