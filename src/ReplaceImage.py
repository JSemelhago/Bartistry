from PIL import Image
import glob

img_path = glob.glob('../output/*.jpg')[0]

img = Image.open(img_path)

pixel = img.resize((16, 16), resample = Image.BILINEAR)

result = pixel.resize(img.size, Image.NEAREST)

result.save('../output/result.png')