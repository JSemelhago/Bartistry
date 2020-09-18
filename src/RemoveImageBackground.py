import cv2
import glob

#Find image
img_path = [glob.glob('../data/'+e) for e in ['*.jpg', '*.jpeg', '*.png']][0][0]

#Load image
img = cv2.imread(img_path)

#Convert to gray scale
gray_scale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#Apply Gaussian blur
blur = cv2.GaussianBlur(gray_scale, (5,5), 0)

#Use Otsu's method to get foreground/background in black and white
threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

#Output image
cv2.imwrite('../output/black_white.jpg', threshold)


