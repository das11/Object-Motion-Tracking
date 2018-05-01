import numpy as np 
import cv2
from cspaceSliders import FilterWindow

img = cv2.imread("im.png")
window = FilterWindow("win", img)
window.show(verbose = True)
