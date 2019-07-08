# import the necessary packages
from imutils import paths
import argparse
import cv2
import sys
import csv
import os

def variance_of_laplacian(image):
	# compute the Laplacian of the image and then return the focus
	# measure, which is simply the variance of the Laplacian
	return cv2.Laplacian(image, cv2.CV_64F,ksize = 5).var()
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", required=True,
	help="path to input directory of images")
ap.add_argument("-t", "--threshold", type=float, default=100.0,
	help="focus measures that fall below this value will be considered 'blurry'")
ap.add_argument("-o", "--out_csv_path", default = os.path.join(os.getcwd(),"test.csv"),
	help="full path to csv file to be created and saved with output")
	
args = vars(ap.parse_args())

# open file to write (cerates it if it doesn't exist)
f = open(args["out_csv_path"], mode='w',newline='')
print("out path: "+args["out_csv_path"])
# create the "writer"
filewriter = csv.writer(f, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
# write header
filewriter.writerow(['path','variance_of_laplacian','blur'])

# loop over the input images
for imagePath in paths.list_images(args["images"]):
	# load the image, convert it to grayscale, and compute the
	# focus measure of the image using the Variance of Laplacian
	# method
	image = cv2.imread(imagePath)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	fm = variance_of_laplacian(gray).round(2)

	if fm > args["threshold"]:
		text = imagePath+" - Not Blurry: "+str(fm)
		filewriter.writerow([imagePath,str(fm),"FALSE"])
		print(imagePath+" - Not Blurry: "+str(fm))
 
	# if the focus measure is less than the supplied threshold,
	# then the image should be considered "blurry"
	if fm < args["threshold"]:
		text = imagePath+" - Blurry: "+str(fm)
		filewriter.writerow([imagePath,str(fm),"TRUE"])
		print(imagePath+" - Blurry: "+str(fm))

