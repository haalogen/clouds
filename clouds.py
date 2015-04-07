#/bin/python

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


im1 = Image.open("S701-0002.JPG")
im2 = Image.open("S702-0002.JPG")

print im1.filename, im1.mode, im1.size
print 
print im2.filename, im2.mode, im2.size
print 

#get width & height
width_orig = im1.size[0]
height_orig  = im1.size[1]


#convert original images to grayscale
im1_gs = im1.convert("L")
im2_gs = im2.convert("L")

# width & height of a piece
width_cropped = 500
height_cropped = 500

# cropped im2 in grayscale; size = (300x300)
im2_piece = im2_gs.crop( (im2.size[0] / 2 - width_cropped/2,
                          im2.size[1] / 3 - height_cropped/2,
                          im2.size[0] / 2 + width_cropped/2,
                          im2.size[1] / 3 + height_cropped/2) )


im2_piece.show()

# Uncomment if want to save cropped fragment of picture
#im2_piece.save("im2_piece_"+str(im2.filename), "JPEG")




