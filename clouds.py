#TODO: PyQt4 GUI: 2 labels, QrubberBand, OpenFileDialogs,
#StartSearchDialog with ability to change parameters,
#After getting result -- ask whether it's correct or should be seached again
#Fine search with parameters
#TODO: alignment (yustirovka) by stars -> affine transform
#!/usr/bin/python
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
import time
import sys

im1 = Image.open("S701-0013.JPG")
im2 = Image.open("S702-0013.JPG")


print im1.filename, im1.mode, im1.size
print 
print im2.filename, im2.mode, im2.size
print 

# width & height of a piece
width_cropped = 200
height_cropped = 200

#absolute(on original image im2) cordinates of cropped_piece 
#(top left corner of square==kvadrat)
x = im2.size[0] * 50/100
y = im2.size[1] * 33/100

# cropped im2 in grayscale; size = (300x300)
im2_piece = im2.crop( ( x - width_cropped/2,
                        y - height_cropped/2,
                        x + width_cropped/2,
                        y + height_cropped/2 ) )

im1_piece = im1.crop( ( x - width_cropped*3/2,
                        y - height_cropped*3/2,
                        x + width_cropped*3/2,
                        y + height_cropped*3/2 ) )
im1_piece.show()
im2_piece.show()

#convert original images to grayscale
im1_piece = im1_piece.convert("L")
im2_piece = im2_piece.convert("L")
#im1_piece.show()
#im2_piece.show()
print "Image1_piece", im1_piece.mode, im1_piece.size
print 
print "Image2_piece", im2_piece.mode, im2_piece.size
print 


num_of_quants = 8
#COLOR QUANTIZATION !!!
im1_piece = im1_piece.convert("P", palette=Image.ADAPTIVE, colors=num_of_quants)
im2_piece = im2_piece.convert("P", palette=Image.ADAPTIVE, colors=num_of_quants)

#im1_piece.show()
#im2_piece.show()
#----------------------------------------------------------------

#Load pixels
pix1 = im1_piece.load()
pix2 = im2_piece.load()


# im1_piece array representation
data1 = np.zeros(im1_piece.size)
data2 = np.zeros(im2_piece.size)

for i in range(im1_piece.size[0]):
    for j in range(im1_piece.size[1]):
        data1[i,j] = np.int8( pix1[i,j] )

for i in range(im2_piece.size[0]):
    for j in range(im2_piece.size[1]):
        data2[i,j] = np.int8( pix2[i,j] )

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
#array representation of pix2
fragment = data2
min_i, min_j = 0, 0
#projection pix2 on field of pix1
pr = np.zeros( im2_piece.size )

start_time = time.time()

inc = (w-w2+1) / 33
print "inc:", inc

for i in range( 0,w-w2+1, inc ):
    for j in range( 0,h-h2+1, inc ):
# Piece of im1_piece to compare with im2_piece
        field = data1[i:i+w2,j:j+h2] 
        pr[:,:] = 0
# Projectioning
        for l in range(num_of_quants):
            pr += (field*indicators[l]).sum()/(indicators[l]**2).sum() * indicators[l]
#Difference functional that we want to minimize
        diff = ( (pr - field)**2 ).sum()

#        Stupid substarction
#        diff = (( field - fragment )**2).sum()

#If it is the very first iteration
        if (i+j == 0):
            min_diff = diff;
#If NOT first iteration
        elif (diff < min_diff):
            min_diff = diff 
            min_i, min_j = i, j
#        print '\r', i, j, diff
        percentage = 100 * i / (w-w2)
        sys.stdout.write('\r row: '+str(i)+" "+str(percentage)+"%")
        sys.stdout.flush()
print
stop_time = time.time()


print "Result:"
print min_i, min_j, min_diff
print "Time to seek:", (stop_time - start_time)

im1_piece_best = im1.crop( (x - width_cropped*3/2 + min_i,
                            y - height_cropped*3/2 + min_j,
                            x - width_cropped*3/2 + min_i+w2,
                            y - height_cropped*3/2 + min_j+h2) )
print "im1_piece.size", im1_piece.size
print "im1_piece_best.size", im1_piece_best.size
im1_piece_best.show()

