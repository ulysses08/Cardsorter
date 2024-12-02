import os
import cv2
import json
import pytesseract
import numpy as np
from pytesseract import Output
from PIL import Image, ImageOps

#Variables
size = (480, 40)
source = (0, 620, 480, 680)
dest = (0, 310, 480, 370)


#Capture image




#DEBUG IMPORT ONLY

im = Image.open("forest.jpg")

im.save("capture.png")

#Process OCR

im = Image.open("capture.png")

region = im.crop(source)

im.paste(region, dest)

ImageOps.fit(im, size).save("idblock.png")

img = cv2.imread("idblock.png")

carddetails = pytesseract.image_to_string(img)

print(carddetails) #Remove after debugging complete

os.remove("idblock.png")

os.remove("capture.png")


#Process the string to an array
