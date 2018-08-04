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

  
### gray scaling
The images should be converted into grey scaled image so that canny edge detection can be used.

after Color Selection          |  Gray Scaled 
:-------------------------:|:-------------------------:
![](https://user-images.githubusercontent.com/31281151/43678297-8b935c56-982e-11e8-8186-d32d5eff0a3c.png)  |  ![](https://user-images.githubusercontent.com/31281151/43678378-ef58df08-982f-11e8-9bdf-150ad1214a1e.png)
