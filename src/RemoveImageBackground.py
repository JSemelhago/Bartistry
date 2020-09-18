import cv2
import numpy as np

#Load image
img = cv2.imread('../data/banana.jpg')

#Convert to gray scale
gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Apply Gaussian blur
blur = cv2.GaussianBlur(gray_scale, (5,5), 0)

#Use Otsu's method to get foreground/background
threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

#Bounding rectangle
x, y, w, h = cv2.boundingRect(threshold)

#Create new rectangle from x y width height (x, y -> x+w, y+h)
new_base = x+w
new_height = y+h

cv2.rectangle(img, (x, y), (new_base, new_height), (36, 255, 12), 2)

cv2.imshow('black_white', threshold)
cv2.waitKey()


