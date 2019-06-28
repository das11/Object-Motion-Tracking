import cv2 
import numpy as np
import math 

def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

if __name__ == "__main__":
    
    i2 = cv2.imread("/Users/Interface/Coding 2/CV/motion_detection/i2.png")
    i = cv2.imread("/Users/Interface/Coding 2/CV/motion_detection/i1.png")

    res = mse(i, i2)
    print(res)

