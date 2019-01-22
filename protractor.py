import numpy as np
import cv2
import queue
import imutils
import math

class Protractor:

	def __init__(self, accepted_varience, camera_source):
		self.accepted_varience = accepted_varience
		self.color_one = None
		self.max_height = 0
		self.camera_source = camera_source
		self.current_img = None
		# self.accepted_varience = (50, 50, 50)

	@staticmethod
	def preprocess_image(img):
		img = imutils.resize(img, width=600)
		img = cv2.GaussianBlur(img, (11, 11), 0)
		img = cv2.GaussianBlur(img, (11, 11), 0)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		return img

	@staticmethod
	def morphology(img):
		img = cv2.erode(img, None, iterations=2)
		img = cv2.dilate(img, None, iterations=2)
		img = cv2.erode(img, None, iterations=2)
		img = cv2.dilate(img, None, iterations=2)
		return img

	@staticmethod
	def find_contours(mask, func):
		contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		contours = imutils.grab_contours(contours)
		return func(contours)


	def run_camera(self):
		cap = cv2.VideoCapture(self.camera_source)
		while(True):
			ret, frame = cap.read()
			cv2.imshow("frame", frame)
			self.current_img = self.preprocess_image(frame)
			cv2.setMouseCallback("frame", self.process_click)
			if self.color_one is not None:
				hight = self.find_contours(self.mask_color(self.morphology), self.draw_rect)
				cv2.imshow("tracking", self.current_img)
				print(self.calc_angle(hight))
			key = cv2.waitKey(1) & 0xFF
			if key == ord("q"):
				break
			elif key == ord("e"):
					print("!!!! RESETING HIGHT VALUE !!!!")
					try:
						self.max_height = hight
					except UnboundLocalError:
						self.max_height = 0

		cap.release()
		cv2.destroyAllWindows()


	def process_click(self, event, x, y, flags, params):
		if event == cv2.EVENT_LBUTTONDOWN:
			self.color_one = self.current_img[x, y]
		

	def mask_color(self, func):
		mask = cv2.inRange(self.current_img, self.color_one - self.accepted_varience, self.color_one + self.accepted_varience)
		mask = func(mask)
		cv2.imshow("mask", mask)
		return mask
		

	def draw_rect(self, contours):
		hight = 1
		if len(contours) > 0:
			rect_contour = max(contours, key=cv2.contourArea)
			rect = cv2.minAreaRect(rect_contour)
			box = cv2.boxPoints(rect)
			x1, y1 = box[0]
			x2, y2 = box[1]
			hight = math.sqrt((x2 - x1) ** 2 + (y2 - y1) **2)
			box = np.int0(box)
			cv2.drawContours(self.current_img, [box], 0, (0, 0, 255), 2)
		return hight

	def calc_angle(self, hight):
		if self.max_height == 0:
			self.max_height = hight
		try:
			return math.degrees(math.acos(hight / self.max_height))
		except ValueError:
			return -1

def main():
	protractor = Protractor((50, 50, 50), 1)
	protractor.run_camera()

if __name__ == '__main__':
	main()