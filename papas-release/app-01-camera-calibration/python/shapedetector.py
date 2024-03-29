import cv2

class ShapeDetector:
	def __init__(self):
		pass
	def detect(self, c):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # if the shape is a triangle, it will have 3 vertices
		objCor = len(approx)
		if objCor == 3:
			shape = "t"
		# if the shape has 4 vertices, it is either a square or
		# a rectangle
		elif objCor == 4:
			# compute the bounding box of the contour and use the
			# bounding box to compute the aspect ratio
			# (x, y, w, h) = cv2.boundingRect(approx)
			# ar = w / float(h)
			# a square will have an aspect ratio that is approximately
			# equal to one, otherwise, the shape is a rectangle
			shape = "s"
			# if ar >= 0.95 and ar <= 1.05 else "rectangle"
		# otherwise, we assume the shape is a circle
		else:
			shape = "c"
		# return the name of the shape
		return shape