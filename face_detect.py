# import the necessary packages
from imutils import face_utils
import numpy as np
import argparse
import imutils
import dlib
import cv2
from scipy.io import savemat


import os
import glob

def process_img(image_fname):
	if os.path.isfile(image_fname):
		# load the input image, resize it, and convert it to grayscale
		image = cv2.imread(image_fname)
		#~ image = cv2.transpose(image)
		image_ref = image
		W = image.shape[1]
		image = imutils.resize(image, width=500)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		# detect faces in the grayscale image
		rects = detector(gray, 1)
		if(len(rects)==0):
			print('{0:s} face not found'.format(image_fname))
		# loop over the face detections
		for (i, rect) in enumerate(rects):
			# determine the facial landmarks for the face region, then
			# convert the facial landmark (x, y)-coordinates to a NumPy
			# array
			shape = predictor(gray, rect)
			shape = face_utils.shape_to_np(shape)
			# convert dlib's rectangle to a OpenCV-style bounding box
			# [i.e., (x, y, w, h)], then draw the face bounding box
			(x, y, w, h) = face_utils.rect_to_bb(rect)
			cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
			# show the face number
			cv2.putText(image, "Face #{}".format(i + 1), (x - 10, y - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
			# loop over the (x, y)-coordinates for the facial landmarks
			# and draw them on the image
			#~ print('id={0:d} npoints={1:d},{2:d}'.format(int(pid),w,h))
			for (x, y) in shape:
				cv2.circle(image, (x, y), 1, (0, 0, 255), -1)
		shape = shape*W/500
		savemat('{0:s}.mat'.format(image_fname[:-4]),{'shape':shape})
		
		cv2.imwrite('{0:s}_check.png'.format(image_fname[:-4]),image)
		# show the output image with the face detections + facial landmarks
		#~ cv2.imshow("Output", image)
		#~ cv2.waitKey(0)
	else:
		print('{0:s} not found'.format(image_fname))

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--folder", help="path to input image folder")
ap.add_argument("-i", "--image", help="path to input image file")
args = vars(ap.parse_args())

# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

if args["folder"] != None:
	flist = glob.glob('{0:s}/*.png'.format(args["folder"]))
	for image_fname in flist:
		process_img(image_fname)
elif args["image"] != None:	
	process_img(args["image"])
else:
	print("Please Specify Folder or image path")
