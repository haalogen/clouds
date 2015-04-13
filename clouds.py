#/bin/python

from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
import time

im1 = Image.open("S701-0013.JPG")
im2 = Image.open("S702-0013.JPG")


print im1.filename, im1.mode, im1.size
print 
print im2.filename, im2.mode, im2.size
print 

# width & height of a piece
width_cropped = 100
height_cropped = 100

# cropped im2 in grayscale; size = (300x300)
im2_piece = im2.crop( ( im2.size[0] / 2 - width_cropped/2,
                        im2.size[1] / 3 - height_cropped/2,
                        im2.size[0] / 2 + width_cropped/2,
                        im2.size[1] / 3 + height_cropped/2 ) )

im1_piece = im1.crop( ( im1.size[0] / 2 - width_cropped,
                        im1.size[1] / 3 - height_cropped,
                        im1.size[0] / 2 + width_cropped,
                        im1.size[1] / 3 + height_cropped ) )
im1_piece.show()
im2_piece.show()
#convert original images to grayscale
im1_piece = im1_piece.convert("L")
im2_piece = im2_piece.convert("L")
im1_piece.show()
im2_piece.show()
print "Image1_piece", im1_piece.mode, im1_piece.size
print 
print "Image2_piece", im2_piece.mode, im2_piece.size
print 


num_of_quants = 4
#COLOR QUANTIZATION !!!
im1_piece = im1_piece.convert("P", palette=Image.ADAPTIVE, colors=num_of_quants)
im2_piece = im2_piece.convert("P", palette=Image.ADAPTIVE, colors=num_of_quants)

im1_piece.show()
im2_piece.show()
#----------------------------------------------------------------

#Load pixels
pix1 = im1_piece.load()
pix2 = im2_piece.load()


# im1_piece array representation
data1 = np.zeros(im1_piece.size)

for i in range(im1_piece.size[0]):
    for j in range(im1_piece.size[1]):
        data1[i,j] = np.int8( pix1[i,j] )

# Color-indicatong functions
indicators = np.zeros( (num_of_quants,im2_piece.size[0],im2_piece.size[1]), dtype=np.int8 )

for i in range(im2_piece.size[0]):
    for j in range(im2_piece.size[1]):
        a = np.int8( pix2[i,j] )
        indicators[a,i,j] = 1;

w = im1_piece.size[0]
h = im1_piece.size[1]
w2 = im2_piece.size[0]
h2 = im2_piece.size[1]
#just one more name for pix2
fragment = pix2
min_i, min_j = 0, 0
#projection pix2 on field of pix1
pr = np.zeros( im2_piece.size )

start_time = time.time()

for i in range( 0,w-w2+1, 1 ):
    for j in range( 0,h-h2+1,1 ):
# Piece of im1_piece to compare with im2_piece
        field = data1[i:i+w2,j:j+h2] 
        pr[:,:] = 0
# Projectioning
        for l in range(num_of_quants):
            pr += (field*indicators[l]).sum()/(indicators[l]**2).sum() * indicators[l]
#Difference functional that we want to minimize
        diff = ( (pr - field)**2 ).sum()
        
#If it is the very first iteration
        if (i+j == 0):
            min_diff = diff;
#If NOT first iteration
        elif (diff < min_diff):
            min_diff = diff 
            min_i, min_j = i, j
        
        print i, j, diff
stop_time = time.time()

print "Result:"
print min_i, min_j, min_diff
print "Time to seek:", (stop_time - start_time)

im1_piece_best = im1_piece.crop( (min_i,min_j,min_i+w2,min_j+h2) )
print im1_piece_best.size
im1_piece_best.show()



