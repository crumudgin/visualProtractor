import numpy as np
import cv2
import queue


def run_camera(camera_source):
	cap = cv2.VideoCapture(camera_source)
	while(True):
		ret, frame = cap.read()

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		edge_frame = canny_edge_detection(gray)
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
	if img[x, y] == 0:
		img[x, y] = 1
		for i in get_index_neighbors(x, y):
			next.put(i)
	return img

def dijkstras_modified(img, x, y, next):
	print(x, y)
	img = dijkstras_modified_helper(img, x, y, next)
	while next.empty() is False:
		x, y = next.get()
		img = dijkstras_modified_helper(img, x, y, next)
	return img

def morphological_closure(img):
	img = cv2.dilate(img, np.ones((3,3)), iterations = 1)
	img = cv2.erode(img, np.ones((3,3)), iterations = 1)
	return img

def pointPolygon(img, contour, x, y):
	raw_dist = np.empty(img.shape, dtype=np.float32)
	for i in range(img.shape[0]):
		for j  in range(img.shape[1]):
			raw_dist[i, j] = cv2.pointPolygonTest(contour)

def isolate_object(img, x, y):
	# img_copy = img.copy()
	img = morphological_closure(img)
	img_copy, contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	colored_img = cv2.cvtColor(img_copy, cv2.COLOR_GRAY2BGR)
	# print(contours)
	minDist = None
	minContour = None
	for contour in contours:
		dist = abs(cv2.pointPolygonTest(contour, (x, y), True))
		if minDist is None or minDist > dist:
			# cv2.drawContours(colored_img, [contour], 0, (0, 255, 0), 3)
			# cv2.imshow("object", colored_img)
			print(dist)
			minDist = dist
			minContour = contour
			# input("hit enter")
	
	cv2.drawContours(colored_img, [minContour], 0, (0, 255, 0), 3)
	# print(img_copy.shape)
	# img_copy = morphological_closure(img_copy)
	# img_copy = cv2.dilate(img_copy, np.ones((3,3)), iterations = 3)
	# img_copy = morphological_closure(img_copy)
	# img_copy = cv2.erode(img_copy, np.ones((3,3)), iterations = 3)
	# img_copy = dijkstras_modified(img_copy, x, y, queue.Queue())
	# for i in range(img_copy.shape[0]):
	# 	for j in range(img_copy.shape[1]):
	# 		if img_copy[i, j] != 1:
	# 			img_copy[i, j] = 0
	# 		else:
	# 			img_copy[i, j] = 255
	cv2.imshow("object", colored_img)

# def find_convex_hull(img):


def process_click(event, x, y, flags, params):
	if event == cv2.EVENT_LBUTTONDOWN:
		isolate_object(process_click.img, y, x)

def main():
	run_camera(0)

if __name__ == '__main__':
	main()