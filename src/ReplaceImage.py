from PIL import Image
import glob
import numpy as np
import pandas as pd

#Find jpg and open it
img_path = glob.glob('../output/*.jpg')[0]
img = Image.open(img_path)

#Convert to be 16 pixels by 16 pixels
result = img.resize((16, 16), Image.ANTIALIAS)

#Convert to dataframe with arrays representing colours
pixel_array = np.array(result)
df = pd.DataFrame(pixel_array.tolist())

#Save dataframe and image
df.to_csv('../output/pixel_array.csv', index=False, header=False)
result.save('../output/result.png')