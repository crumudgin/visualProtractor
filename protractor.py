import numpy as np
import cv2
import imutils
import math

"""
Class to measure the angle of an object in an image
"""
class Protractor:


	"""
	Parameters: accepted_varience - the acceptable variance within the color space
				camera_source - the camera to read from
				morphology_func - any function that takes a image and returns a black and white image
				shape_func -  any function that takes contours and and an image, and returns an integer
	"""
	def __init__(self, accepted_varience, camera_source, morphology_func = None, shape_func = None):
		self.accepted_varience = accepted_varience
		self.camera_source = camera_source
		self.set_funcs(morphology_func, shape_func)
		self.color_one = None
		self.max_height = 0
		self.current_img = None
		
		

	"""
	Parameters: img - the image to preprocess
	Returns: the preprocessed image
	Description: Performs necessary operations on the provided image before object detection can be performed
	"""
	@staticmethod
	def preprocess_image(img, blurs):
		for i in range(blurs):
			img = cv2.GaussianBlur(img, (11, 11), 0)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		return img

	"""
	Parameters: img - the black and white image to apply the morphology too
				rounds - the number of times the morphology should be applied
	Returns: the image with the given morphology applied
	Description: Closes small unnatural gaps in a black and white image
	"""
	@staticmethod
	def morphology(img, rounds = 1):
		for i in range(rounds):
			img = cv2.erode(img, None, iterations=2)
			img = cv2.dilate(img, None, iterations=2)
		return img

	"""
	Parameters: mask - the black and white image who's contours will be discovered
	Returns: the contours of the provided mask
	Description: fins the contours of the provided image so the object can be found within the image
	"""
	@staticmethod
	def find_contours(mask):
		contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		contours = imutils.grab_contours(contours)
		return contours

	"""
	Parameters: contours - the contours of the image that the rectangle will be extracted from
	Returns - the hight of the rectangle
	Description - finds a rectangle based on the contours and calculates it's hight
	"""
	@staticmethod
	def draw_rect(contours, current_img):
		hight = 1 # 1 is the default to avoid dividing by 0
		if len(contours) > 0:
			rect_contour = max(contours, key=cv2.contourArea)
			rect = cv2.minAreaRect(rect_contour)
			box = cv2.boxPoints(rect)
			x1, y1 = box[0]
			x2, y2 = box[1]
			hight = math.sqrt((x2 - x1) ** 2 + (y2 - y1) **2)
			box = np.int0(box)
			cv2.drawContours(current_img, [box], 0, (0, 0, 255), 2)
		return hight


	"""
	Description: Opens the camera feed and manages the feed loop and the inputs the feed may receive
	"""
	def run_camera(self):
		feed = cv2.VideoCapture(self.camera_source)
		while(True):
			hight = self.process_camera_feed(feed)
			key = cv2.waitKey(1) & 0xFF
			if key == ord("q"):
				break
			elif key == ord("r"):
					print("!!!! RESETING HIGHT VALUE !!!!")
					try:
						self.max_height = hight
					except UnboundLocalError:
						self.max_height = 0

		feed.release()
		cv2.destroyAllWindows()

	def set_funcs(self, morphology_func = None, shape_func = None):
		self.morphology_func = morphology_func
		if morphology_func is None:
			self.morphology_func = self.morphology
		self.shape_func = shape_func
		if shape_func is None:
			self.shape_func = draw_rect

	"""
	Parameters: feed - the image feed to process
	Returns: the result of the desired calculation
	Description: does all the required operations to find/track an object and calculate its relative angle
	"""
	def process_camera_feed(self, feed):
		_, frame = feed.read()
		cv2.imshow("frame", frame)
		self.current_img = self.preprocess_image(frame, 2)
		cv2.setMouseCallback("frame", self.process_click)
		hight = 1
		if self.color_one is not None:
			hight = self.calc_hight()
			cv2.imshow("tracking", self.current_img)
			print(self.calc_angle(hight))
		return hight

	"""
	Parameters: event - the event that has taken place
				x - the x coordinate of the event location
				y - the y coordinate of the event location
				flags - required for the function call, has no effect on the logic
				params - required for the function call, has no effect on the logic
	"""
	def process_click(self, event, x, y, flags, params):
		if event == cv2.EVENT_LBUTTONDOWN:
			self.color_one = self.current_img[x, y]
		

	"""
	Parameters: func - an optional function to be applied on the mask to complete the masking process
				func_params - any params the function may need
	Returns: the processed black and white mask
	Description: sets all pixels that are within the accepted variance of the provided pixel to 255 and the rest to 0
	"""
	def mask_color(self, func = None):
		mask = cv2.inRange(self.current_img, self.color_one - self.accepted_varience, self.color_one + self.accepted_varience)
		if func is not None:
			mask = func(mask)
		cv2.imshow("mask", mask)
		return mask
		

	"""
	Returns - the hight of the object being tracked
	Description - performs all operations required to track an object within the image and calculates that objects hight
	"""
	def calc_hight(self):
		mask = self.mask_color(self.morphology_func)
		contours = self.find_contours(mask)
		hight = self.shape_func(contours, self.current_img)
		return hight

	"""
	Parameters: hight - the hight of the object being tracked
	Returns: the relative angle of the object
	Description: calculates the relative angle of the tracked object with the initial hight (or hight on reset) being the initial starting
				 position, and the current hight being the relative position
	"""
	def calc_angle(self, hight):
		if self.max_height == 0:
			self.max_height = hight
		try:
			return math.degrees(math.acos(hight / self.max_height))
		except ValueError:
			return -1

def main():
	protractor = Protractor((50, 50, 50), 1, lambda mask: Protractor.morphology(mask, 2) , Protractor.draw_rect)
	protractor.run_camera()

if __name__ == '__main__':
	main()