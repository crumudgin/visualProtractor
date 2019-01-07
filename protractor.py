import numpy as np
import cv2
import queue


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
	edges = cv2.Canny(img, 100, 110)
	cv2.imshow("frame", edges)
	process_click.img = edges
	cv2.setMouseCallback("frame", process_click)
	return edges

def get_index_neighbors(x, y):
	if x < 479 and y < 639 and x > 1 and y > 1:
		return ((x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y))
	else:
		return []

def dijkstras_modified_helper(img, x, y, next):
	# print(x, y)
	if img[x, y] == 0:
		img[x, y] = 255
		# if len([j for j in get_index_neighbors(x, y) if img[j[0], j[1]] == 0]) == 4:

		for i in get_index_neighbors(x, y):
			next.put(i)
	# else:
	# 	print(img[x, y])
	return img

def dijkstras_modified(img, x, y, next):
	print(x, y)
	img = dijkstras_modified_helper(img, x, y, next)
	# counter = 100000
	while next.empty() is False:
		# if counter <= 0:
			# return img
		x, y = next.get()
		img = dijkstras_modified_helper(img, x, y, next)
		# counter -= 1
	return img

def isolate_object(img, x, y):
	# make matrix of zeros in the same shape as the image
	# starting at the x, y coordanites dijkstras out until you hit an edge
	# the result will be the inner area of the edge
	img_copy = img.copy()
	print(img_copy.shape)
	img_copy = cv2.dilate(img_copy, np.ones((3,3)), iterations = 1)
	img_copy = cv2.erode(img_copy, np.ones((3,3)), iterations = 1)
	img_copy = cv2.dilate(img_copy, np.ones((3,3)), iterations = 3)
	img_copy = cv2.erode(img_copy, np.ones((3,3)), iterations = 1)
	img_copy = cv2.dilate(img_copy, np.ones((3,3)), iterations = 1)
	img_copy = dijkstras_modified(img_copy, x, y, queue.Queue())
	cv2.imshow("object", img_copy)

def process_click(event, x, y, flags, params):
	if event == cv2.EVENT_LBUTTONDOWN:
		isolate_object(process_click.img, y, x)

def main():
	run_camera(1)

if __name__ == '__main__':
	main()