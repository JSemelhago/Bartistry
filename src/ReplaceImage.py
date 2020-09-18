from PIL import Image
import glob
import numpy as np
import pandas as pd

#Find jpg and open it
img_path = glob.glob('../output/*.jpg')[0]
img = Image.open(img_path)


base = 20
percent = (base/float(img.size[0]))
height = int((float(img.size[1])*float(percent)))

#TODO: Make this proportional to image size
result = img.resize((base, height), Image.ANTIALIAS)

#Convert to dataframe with arrays representing colours
pixel_array = np.array(result)
df = pd.DataFrame(pixel_array.tolist())

#Save dataframe and image
df.to_csv('../output/pixel_array.csv', index=False, header=False)
result.save('../output/result.png')