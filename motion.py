from collections import deque
import numpy as np
import argparse 
import imutils 
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video")
ap.add_argument("-b", "--buffer", default = 32)

args = vars(ap.parse_args())

greenLower = (171,  92,  95)
greenUpper = (179, 206, 255)

pts = deque(maxlen = 32)

counter = 0
(dX, dY) = (0,0)
direction = ""

if not args.get("video", False):
	camera = cv2.VideoCapture(0)
else:
	camera = cv2.VideoCapture(args["video"])

img = np.zeros((512,512,3), np.uint8);

def poly(point) : 

	i = 0
	init = point
	++i

	if i > 0 :
		cv2.line(img, init, point, Scalar(0, 255, 0), 1, CV_AA)


while True:

	(grabbed, frame) = camera.read()

	if args.get("video") and not grabbed:
		break

	frame = imutils.resize(frame, width=600)
	blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	cv2.imshow("fr", mask)

	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	if len(cnts) > 0:

		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		if radius > 10:
			cv2.circle(frame, (int(x), int(y)), int(radius),
				(0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)
			pts.appendleft(center)
			poly(pts)

	for i in np.arange(1, len(pts)):
		if pts[i-1] is None or pts[i] is None:
			continue

		if counter >= 10 and i == 10 and pts[i-10] is not None:
			
			dX = pts[-10][0] - pts[i][0]
			dY = pts[-10][1] - pts[i][1]
			(dirX, dirY) = ("", "")
 
			if np.abs(dX) > 20:
				dirX = "East" if np.sign(dX) == 1 else "West"
 
			if np.abs(dY) > 20:
				dirY = "North" if np.sign(dY) == 1 else "South"
 
			if dirX != "" and dirY != "":
				direction = "{}-{}".format(dirY, dirX)
 
			else:
				direction = dirX if dirX != "" else dirY

			thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
			cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)
 
	cv2.putText(frame, direction, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
		0.65, (0, 0, 255), 3)
	cv2.putText(frame, "dx: {}, dy: {}".format(dX, dY),
		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.35, (0, 0, 255), 1)
 
	
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF
	counter += 1
	
	if key == ord("q"):
		print(c)
		break

camera.release()
cv2.destroyAllWindows()

