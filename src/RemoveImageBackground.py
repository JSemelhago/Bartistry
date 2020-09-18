import cv2
import glob
import numpy as np
import matplotlib.pyplot as plt

#Find image
img_path = [glob.glob('../data/'+e) for e in ['*.jpg', '*.jpeg', '*.png']][0][0]

#Load image
img = cv2.imread(img_path)

mask = np.zeros(img.shape[:2], np.uint8)

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

img_copy = img.copy()

#Convert to gray scale
gray_scale = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

binary = cv2.bitwise_not(gray_scale)

contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

rect = (0,0,0,0)

for contour in contours:
    (x,y,w,h) = cv2.boundingRect(contour)
    rect = (x,y,w,h)
    cv2.rectangle(img_copy, (x,y), (x+w,y+h), (0,255,0), 2)

print(rect)


cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
mask2 = np.where((mask==2)+(mask==0),255,0).astype('uint8')
img = img*mask2[:,:,np.newaxis]

plt.imshow(img)
plt.colorbar()
plt.show()


# #Apply Gaussian blur
# blur = cv2.GaussianBlur(gray_scale, (5,5), 0)
#
# #Use Otsu's method to get foreground/background in black and white
# threshold = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

#Output image
cv2.imwrite('../output/black_white.jpg', img)


