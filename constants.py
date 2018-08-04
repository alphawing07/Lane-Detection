import numpy as np 

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