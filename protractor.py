import numpy as np
import cv2
# import argparse


def run_camera(camera_source):
	cap = cv2.VideoCapture(camera_source)
	while(True):
		ret, frame = cap.read()

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# cv2.imshow("frame", gray)
		edge_frame = canny_edge_detection(gray)
		# cv2.namedWindow("edges")
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break

	cap.release()
	cv2.destroyAllWindows()

def canny_edge_detection(img):
	edges = cv2.Canny(img, 100, 200)
	cv2.imshow("frame", edges)
	process_click.img = edges
	cv2.setMouseCallback("frame", process_click)
	return edges

# def isolate_object(img, x, y):
	#make matrix of zeros in the same shape as the image
	#starting at the x, y coordanites dijkstras out until you hit an edge
	#the result will be the inner area of the edge

def process_click(event, x, y, flags, params):
	if event == cv2.EVENT_LBUTTONDOWN:
		print("clickety")

def main():
	run_camera(1)

if __name__ == '__main__':
	main()