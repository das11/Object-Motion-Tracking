import cv2
import numpy as np 

def estimate_intensity(frame):
	avg_intensity = cv2.mean(frame)

	return avg_intensity


def detect_thresh(intensity):

	# intensity = estimate_intensity(frame)

	# return intensity
	if intensity in range(70, 185):
		return 90

	elif intensity in range(9, 69):
		return 70

	elif intensity in range(1, 8):
		return 2

