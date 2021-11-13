"""
Coin Detection(coiny) Model1 
"""


"""
Importing open CV, numpy and matplotlib
"""
import cv2
import numpy as np
import matplotlib.pyplot as plt


"""
Reading the image
"""
rupee1 = cv2.imread('images (1).jpg',1)
from google.colab.patches import cv2_imshow
cv2_imshow(rupee1)


"""
Converting the image to Grayscale
"""
img = cv2.cvtColor(rupee1, 
		 cv2.COLOR_BGR2GRAY)
plt.rcParams["figure.figsize"] = (16,9)
plt.imshow(img,cmap='gray')


"""
Blurring the image using GaussianBlur
"""
img = cv2.GaussianBlur(img, 
		      (21,21), 
	              cv2.BORDER_DEFAULT)
plt.rcParams["figure.figsize"] = (16,9)
plt.imshow(img,cmap='gray')


"""
Finally applying HoughCircles on the preprocessed image
"""
circles = cv2.HoughCircles(img, 
			   cv2.HOUGH_GRADIENT, 
                           0.9, 
		           20, 
                           param1=50, 
	                   param2=30, 
			   minRadius=0, 
		           maxRadius=0)
detected_circles = np.uint16(np.around(circles))
for (x,y,r) in detected_circles[0,:]:
  cv2.circle(rupee1, 
             (x,y), 
	      r,  
             (0,255,0), 
	      3)
  cv2.circle(rupee1,
	     (x,y), 
	      2, 
	     (0,255,255),
	      3)


"""
Outputting the image(since the code is wriiten in google colab, 'google.colab.patches' library is used)
"""
from google.colab.patches import cv2_imshow
plt.rcParams["figure.figsize"] = (16,9)
cv2_imshow(rupee1)
