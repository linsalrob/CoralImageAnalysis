import sys
sys.path.append('../Modules/')
import cv2
import ImageIO
import Normalization
from matplotlib import pyplot as plt
import numpy

'''
A test program to make sure that the Normalization methods work.

This normalizes the images, and displays them.
'''

test = 'test.jpg'
#test = "/home/redwards/Dropbox/ComputerVision/TestCode/test.png"
im = ImageIO.cv2read(test)
print im.shape


print "Testing Tylers normalization"
tn = Normalization.Tyler(im)

print "Testing histogram equalization"
he = Normalization.equalizeHistograms(im)
heo = numpy.ones_like(im)
heo[:,:,0]=he
heo[:,:,1]=he
heo[:,:,2]=he

print "Simple normaliztion"
nh = Normalization.simpleNorm(im)
print nh.shape

partone = numpy.vstack([im, heo])
parttwo = numpy.vstack([tn, nh])

allim = numpy.hstack([partone, parttwo])

print "Press any key to exit\n"
cv2.imshow('images', allim)
#cv2.imshow('grey', he)
cv2.waitKey(0)
cv2.destroyAllWindows()

