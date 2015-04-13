#/bin/python

from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt


num_of_quants = 64
im1 = Image.open("S701-0013.JPG")
im2 = Image.open("S702-0013.JPG")


print im1.filename, im1.mode, im1.size
print 
print im2.filename, im2.mode, im2.size
print 

# width & height of a piece
width_cropped = 400
height_cropped = 400

# cropped im2 in grayscale; size = (300x300)
im2_piece = im2.crop( ( im2.size[0] / 2 - width_cropped/2,
                        im2.size[1] / 3 - height_cropped/2,
                        im2.size[0] / 2 + width_cropped/2,
                        im2.size[1] / 3 + height_cropped/2 ) )

im1_piece = im1.crop( ( im1.size[0] / 2 - width_cropped,
                        im1.size[1] / 3 - height_cropped,
                        im1.size[0] / 2 + width_cropped,
                        im1.size[1] / 3 + height_cropped ) )

im1_piece_ind = np.zeros( (3,im1_piece.size[0], im1_piece.size[1]), dtype = np.int16 )
im1_piece_ind = im1_piece.split()
im1_piece_ind[0].show()

#Uncomment to show the cropped piece
#im1_piece.show(title="The im1`cropped piece")
#im2_piece.show(title="The im2 cropped piece")

# Uncomment if want to save cropped fragment of picture
#im2_piece.save("im2_piece_"+str(im2.filename), "JPEG")

#Load pixels
pix1 = im1_piece.load()
pix2 = im2_piece.load()


# Create a tool for drawing in im1
draw1 = ImageDraw.Draw(im1_piece) 
draw2 = ImageDraw.Draw(im2_piece)

for i in range(im1_piece.size[0]):
    for j in range(im1_piece.size[1]):
        r = int( pix1[i,j][0] )
        g = int( pix1[i,j][1] )
        b = int( pix1[i,j][2] )
        
        s = (r+g+b) / 3
        draw1.point( (i,j), (s,s,s) )



for i in range(im2_piece.size[0]):
    for j in range(im2_piece.size[1]):
        r = int( pix2[i,j][0] )
        g = int( pix2[i,j][1] )
        b = int( pix2[i,j][2] )
        
        s = (r+g+b) / 3
        draw2.point( (i,j), (s,s,s) )


#Convert pieces to GRAYSCALE
im1_piece.convert("L")
im2_piece.convert("L")
#im2_piece.show("im2_piece in GRAYSCALE")



# Color statictics of a piece
color_stat = np.zeros(500, dtype=int)
x = np.arange(0,500)


for i in range(im2_piece.size[0]):
    for j in range(im2_piece.size[1]):
# color statistics on red, green, blue spectra
        color_stat[ pix2[i,j][0] ] += 1



print "Piece of image2. Before color quantization: "
print
print color_stat
print

#Uncomment to show COLOR_STATISTICS graph
plt.plot(x, color_stat, 'r')
plt.show()  



#COLOR QUANTIZATION !!!

im1_piece = im1_piece.convert("P", palette=Image.ADAPTIVE, colors=num_of_quants)
im2_piece = im2_piece.convert("P", palette=Image.ADAPTIVE, colors=num_of_quants)
#Uncomment to see quantized piece of image2
#im2_piece.show(title="quantized piece of image2")


color_stat_quant = np.zeros( num_of_quants , dtype=int)
x2 = np.arange(0,num_of_quants) 


for i in range(im2_piece.size[0]):
    for j in range(im2_piece.size[1]):
        r = int( pix2[i,j][0] )
        g = int( pix2[i,j][1] )
        b = int( pix2[i,j][2] )
        #color statistics on red, green, blue spectra
        color_stat_quant[r] += 1


print "Piece of image2. After color quantization. Colors: ", num_of_quants
print
print color_stat_quant
print

#Uncomment to show COLOR_STATISTICS graph
plt.plot(x2, color_stat_quant)
plt.show()



#w = im1_gs.size[0]
#h = im1_gs.size[1]
#w2 = im2_piece.size[0]
#h2 = im2_piece.size[1]
#fragment = pix2

#min_i, min_j = 0, 0

#for i in range( 0,w-w2+1, w2 ):
#    for j in range( 0,h-h2+1,h2 ):
## Piece of im1_gs to compare with im2_piece
#        field =  data1[i:i+w2,j:j+h2] 
#        
#        pr = np.zeros_like( field )
## Projectioning
#        for l in range(num_of_quants):
#            pr += (field*indicators[l]).sum()/(indicators[l]**2).sum() * indicators[l]
##Difference functional that we want to minimize
#        diff = ( (pr - field)**2 ).sum()

##If it is the very first iteration
#        if (i+j == 0):
#            min_diff = diff;
##If NOT first iteration
#        elif (diff < min_diff):
#            min_diff = diff 
#            min_i, min_j = i, j
#        
#        print i, j, diff
#print
# 

#im1_piece = im1_gs.crop( (min_i,min_j,min_i+w2,min_j+h2) )

#print "Original:"
#print im2.size[0] / 2 - width_cropped/2, im2.size[1] / 3 - height_cropped/2
#print "Result:"
#print min_i, min_j, min_diff

#im1_piece.show(title="Im1_piece")
#im2_piece.show(title="Im2_piece")




