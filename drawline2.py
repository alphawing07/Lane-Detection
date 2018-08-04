import math
import cv2
import numpy as np

def perp( a ) :
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b
def seg_intersect(a1,a2, b1,b2):
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = np.dot( dap, db)
    num = np.dot( dap, dp )
    return (num / denom.astype(float))*db + b1

avgLeft = (0, 0, 0, 0)
avgRight = (0, 0, 0, 0)
def movingAverage(avg, new_sample, N=20):
    if (avg == 0):
        return new_sample
    avg -= avg / N;
    avg += new_sample / N;
    return avg;
def  drawline2(img,lines, color = [255,0,0], thickness=10):
        largestLeftLineSize = 0
        largestRightLineSize = 0
        largestLeftLine = (0,0,0,0)
        largestRightLine = (0,0,0,0)
        avgLeft = (0, 0, 0, 0)
        avgRight = (0, 0, 0, 0)
        
        if lines is None:
            avgx1, avgy1, avgx2, avgy2 = avgLeft
            cv2.line(img, (int(avgx1), int(avgy1)), (int(avgx2), int(avgy2)), [255,255,255], 12) #draw left line
            avgx1, avgy1, avgx2, avgy2 = avgRight
            cv2.line(img, (int(avgx1), int(avgy1)), (int(avgx2), int(avgy2)), [255,255,255], 12) #draw right line
            return
        
        for line in lines:
            for x1,y1,x2,y2 in line:
                size = math.hypot(x2 - x1, y2 - y1)
                slope = ((y2-y1)/(x2-x1))
                # Filter slope based on incline and
                # find the most dominent segment based on length
                if (slope > 0.5): #right
                    if (size > largestRightLineSize):
                        largestRightLine = (x1, y1, x2, y2)                    
                    cv2.line(img, (x1, y1), (x2, y2), color, thickness)
                elif (slope < -0.5): #left
                    if (size > largestLeftLineSize):
                        largestLeftLine = (x1, y1, x2, y2)
                    cv2.line(img, (x1, y1), (x2, y2), color, thickness)

        # Define an imaginary horizontal line in the center of the screen
        # and at the bottom of the image, to extrapolate determined segment
        imgHeight, imgWidth = (img.shape[0], img.shape[1])
        upLinePoint1 = np.array( [0, int(imgHeight - (imgHeight/3))] )
        upLinePoint2 = np.array( [int(imgWidth), int(imgHeight - (imgHeight/3))] )
        downLinePoint1 = np.array( [0, int(imgHeight)] )
        downLinePoint2 = np.array( [int(imgWidth), int(imgHeight)] )
        
        # Find the intersection of dominant lane with an imaginary horizontal line
        # in the middle of the image and at the bottom of the image.
        p3 = np.array( [largestLeftLine[0], largestLeftLine[1]] )
        p4 = np.array( [largestLeftLine[2], largestLeftLine[3]] )
        upLeftPoint = seg_intersect(upLinePoint1,upLinePoint2, p3,p4)
        downLeftPoint = seg_intersect(downLinePoint1,downLinePoint2, p3,p4)
        if (math.isnan(upLeftPoint[0]) or math.isnan(downLeftPoint[0])):
            avgx1, avgy1, avgx2, avgy2 = avgLeft
            cv2.line(img, (int(avgx1), int(avgy1)), (int(avgx2), int(avgy2)), [255,255,255], 12) #draw left line
            avgx1, avgy1, avgx2, avgy2 = avgRight
            cv2.line(img, (int(avgx1), int(avgy1)), (int(avgx2), int(avgy2)), [255,255,255], 12) #draw right line
            
            return
        cv2.line(img, (int(upLeftPoint[0]), int(upLeftPoint[1])), (int(downLeftPoint[0]), int(downLeftPoint[1])), [0, 0, 255], 8) #draw left line

        # Calculate the average position of detected left lane over multiple video frames and draw
        
        avgx1, avgy1, avgx2, avgy2 = avgLeft
        avgLeft = (movingAverage(avgx1, upLeftPoint[0]), movingAverage(avgy1, upLeftPoint[1]), movingAverage(avgx2, downLeftPoint[0]), movingAverage(avgy2, downLeftPoint[1]))
        avgx1, avgy1, avgx2, avgy2 = avgLeft
        cv2.line(img, (int(avgx1), int(avgy1)), (int(avgx2), int(avgy2)), [255,255,255], 12) #draw left line

        # Find the intersection of dominant lane with an imaginary horizontal line
        # in the middle of the image and at the bottom of the image.
        p5 = np.array( [largestRightLine[0], largestRightLine[1]] )
        p6 = np.array( [largestRightLine[2], largestRightLine[3]] )
        upRightPoint = seg_intersect(upLinePoint1,upLinePoint2, p5,p6)
        downRightPoint = seg_intersect(downLinePoint1,downLinePoint2, p5,p6)
        if (math.isnan(upRightPoint[0]) or math.isnan(downRightPoint[0])):
            avgx1, avgy1, avgx2, avgy2 = avgLeft
            cv2.line(img, (int(avgx1), int(avgy1)), (int(avgx2), int(avgy2)), [255,255,255], 12) #draw left line
            avgx1, avgy1, avgx2, avgy2 = avgRight
            cv2.line(img, (int(avgx1), int(avgy1)), (int(avgx2), int(avgy2)), [255,255,255], 12) #draw right line
            return
        cv2.line(img, (int(upRightPoint[0]), int(upRightPoint[1])), (int(downRightPoint[0]), int(downRightPoint[1])), [0, 0, 255], 8) #draw left line

        # Calculate the average position of detected right lane over multiple video frames and draw
        
        avgx1, avgy1, avgx2, avgy2 = avgRight
        avgRight = (movingAverage(avgx1, upRightPoint[0]), movingAverage(avgy1, upRightPoint[1]), movingAverage(avgx2, downRightPoint[0]), movingAverage(avgy2, downRightPoint[1]))
        avgx1, avgy1, avgx2, avgy2 = avgRight
        cv2.line(img, (int(avgx1), int(avgy1)), (int(avgx2), int(avgy2)), [255,255,255], 12) #draw left line
