import numpy as np
import cv2
# from matplotlib import pyplot as plt


def run_camera(camera_source):
	cap = cv2.VideoCapture(camera_source)
	while(True):
		ret, frame = cap.read()

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# cv2.imshow("frame", gray)
		canny_edge_detection(gray)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break

	cap.release()
	cv2.destroyAllWindows()

def canny_edge_detection(img):
	edges = cv2.Canny(img, 100, 200)
	cv2.imshow("frame", edges)

run_camera(1)