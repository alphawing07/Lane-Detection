# Lane-Detection

## OVERVIEW
This project aims at detecting lanes on road in real time using Computer Vision.

Original          |  Result
:-------------------------:|:-------------------------:
![](https://github.com/alphawing07/Lane-Detection/blob/master/test/solidYellowCurve.jpg)  |  ![](https://github.com/alphawing07/Lane-Detection/blob/master/output/solidYellowCurve.jpg)


## PIPELINE
  ### Color Selection
  Selecting only yellow and white colors in the images using the RGB channels.
  
  Original          |  after Color Selection
:-------------------------:|:-------------------------:
![](https://github.com/alphawing07/Lane-Detection/blob/master/test/solidYellowCurve.jpg)  |  ![](https://user-images.githubusercontent.com/31281151/43678297-8b935c56-982e-11e8-8186-d32d5eff0a3c.png)

  
### Gray Scaling
The images should be converted into grey scaled image so that canny edge detection can be used.

after Color Selection          |  Gray Scaled 
:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/31281151/43678297-8b935c56-982e-11e8-8186-d32d5eff0a3c.png)  |  ![](https://user-images.githubusercontent.com/31281151/43678378-ef58df08-982f-11e8-9bdf-150ad1214a1e.png)
### Gaussian Blur
To remove the noise and make edges smoother

Gray Scaled         |  Post Gaussian Blur
:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/31281151/43678378-ef58df08-982f-11e8-9bdf-150ad1214a1e.png)  |  ![](https://user-images.githubusercontent.com/31281151/43679077-69285550-983c-11e8-9d21-178d6ecfaad0.png)
### Edge Detection
Detecting edges

Post Gaussian Blur         |  Edge Detection
:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/31281151/43679077-69285550-983c-11e8-9d21-178d6ecfaad0.png) |  ![](https://user-images.githubusercontent.com/31281151/43679130-6a448188-983d-11e8-8de5-bd9173915fd6.png)

### Region of Interest Selection
Applying mask to the surroundings

Edge Detection         |  Post ROI
:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/31281151/43679130-6a448188-983d-11e8-8de5-bd9173915fd6.png)|![](https://user-images.githubusercontent.com/31281151/43679168-36b64ee0-983e-11e8-85df-f7644c721db5.png)

### Hough Transform Line Detection
Using <cv2.HoughLinesP> to detect lines in the edge images and plotting them using user defined Drawline function .

Post ROI        |  Line Detection
:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/31281151/43679168-36b64ee0-983e-11e8-85df-f7644c721db5.png)|![](https://user-images.githubusercontent.com/31281151/43679208-2c5a5e7c-983f-11e8-9b2e-6dc0069324b4.png)

#### Finally returning the annotated image 


<img src="https://github.com/alphawing07/Lane-Detection/blob/master/output/solidYellowCurve.jpg" height="320" width="400">








