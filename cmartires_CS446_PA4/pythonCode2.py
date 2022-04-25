#Set up a docker environment for this code, and don't try to include superfluous 
#packages!
from PIL import Image, ImageDraw
import csv
from scipy import constants
import numpy as np

color = 128 * np.ones(shape=[3], dtype=np.uint8)
tuplevals = tuple(color)
im = Image.new('RGB', (512, 512), tuplevals)
draw = ImageDraw.Draw(im)
draw.rectangle((200, 100, 300, 200), fill=(0, 192, 192), outline=(255, 255, 255))
draw.text((100, 200), "You did it!", fill=(int(constants.speed_of_light), 0, 0))
im.save( "pythonCode2Image.png")

try:
    with open('temp.csv', 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
except:
    pass
#modify this code so that it also generates self signed certificate and keys