#TODO: pixel -> int value ??? DONE
#TODO: projection, difference CHECK!!
#TODO: check algorithm AGAIN!!!
#TODO: parallel python
#TODO: pyQT gui

#/bin/python

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


num_of_quants = 64
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
width_cropped = 300
height_cropped = 300

# cropped im2 in grayscale; size = (300x300)
im2_piece = im2_gs.crop( (im2.size[0] / 2 - width_cropped/2,
                          im2.size[1] / 3 - height_cropped/2,
                          im2.size[0] / 2 + width_cropped/2,
                          im2.size[1] / 3 + height_cropped/2) )


#Uncomment to show the cropped piece
im2_piece.show()

# Uncomment if want to save cropped fragment of picture
#im2_piece.save("im2_piece_"+str(im2.filename), "JPEG")


#Load pixels
pix = im2_piece.load()

# Color statictics of a piece
color_stat = np.zeros(1000, dtype=int)
x = np.arange(0,1000)


for i in range(im2_piece.size[0]):
    for j in range(im2_piece.size[1]):
         a = int( pix[i,j] )
         color_stat[a] += 1


print "Piece of image2. Before color quantization: "
print
print color_stat
print

plt.plot(x, color_stat)
plt.show()  


#COLOR QUANTIZATION !!!

im2_piece = im2_piece.convert("P", palette=Image.ADAPTIVE, colors=num_of_quants)

im1_gs = im1_gs.convert("P", palette=Image.ADAPTIVE, colors=num_of_quants)
#Uncomment to see quantized piece of image2
#im2_piece.show()

#Load pixels
pix2 = im2_piece.load()
pix = im1_gs.load()

color_stat2 = np.zeros(num_of_quants, dtype=int)
x2 = np.arange(0,num_of_quants) 

# Color-indicatong functions
indicators = np.zeros( (num_of_quants,im2_piece.size[0],im2_piece.size[1]), dtype=np.int8 )


for i in range(im2_piece.size[0]):
    for j in range(im2_piece.size[1]):
        a = int( pix2[i,j] )
        color_stat2[a] += 1
        indicators[a,i,j] = 1;

# im1_gs as an array
data1 = np.zeros(im1_gs.size)
for i in range(im1_gs.size[0]):
    for j in range(im1_gs.size[1]):
        data1[i,j] = int( pix[i,j] )



print "Piece of image2. After color quantization. Colors: ", num_of_quants
print
print color_stat2
print

plt.plot(x2, color_stat2)
plt.show()



w = im1_gs.size[0]
h = im1_gs.size[1]
w2 = im2_piece.size[0]
h2 = im2_piece.size[1]
fragment = pix2

min_i, min_j = 0, 0

for i in range( 0,w-w2+1, w2/10 ):
    for j in range( 0,h-h2+1,h2/10 ):
# Piece of im1_gs to compare with im2_piece
        field =  data1[i:i+w2,j:j+h2] 
        
        pr = np.zeros_like( field )
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
print
 

im1_piece = im1_gs.crop( (min_i,min_j,min_i+w2,min_j+h2) )

print "Original:"
print 
print "Result:"
print min_i, min_j, min_diff

im1_piece.show(title="Im1_piece")
im2_piece.show(title="Im2_piece")




