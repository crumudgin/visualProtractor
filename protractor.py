import numpy as np
import cv2
import queue
import imutils


ACCEPED_VARIENCE = (30, 30, 30)

COLOR_ONE = None


### MASK BACKGROUND COLORS
### INVERT THE MASKED IMAGE
### DRAW RECTANGLE ARROUND OBJECT
### MEASURE LENGTH
### DO TRIG
### REPEATE

def run_camera(camera_source):
	cap = cv2.VideoCapture(camera_source)
	while(True):
		ret, frame = cap.read()
		cv2.imshow("frame", frame)
		img = preprocess_image(frame)
		if COLOR_ONE is not None:
			mask_color(img)

		# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# edge_frame = canny_edge_detection(gray)
		if cv2.waitKey(1) & 0xFF == ord("q"):
			break

	cap.release()
	cv2.destroyAllWindows()


def process_click(event, x, y, flags, params):
	global COLOR_ONE
	if event == cv2.EVENT_LBUTTONDOWN:
		print(process_click.img[x, y])
		COLOR_ONE = process_click.img[x, y]

def preprocess_image(img):
	img = imutils.resize(img, width=600)
	img = cv2.GaussianBlur(img, (11, 11), 0)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	process_click.img = img
	cv2.setMouseCallback("frame", process_click)
	return img

def mask_color(img):
	mask = cv2.inRange(img, COLOR_ONE - ACCEPED_VARIENCE, COLOR_ONE + ACCEPED_VARIENCE)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	cv2.imshow("mask", mask)
	return mask

def main():
	run_camera(0)

if __name__ == '__main__':
	main()