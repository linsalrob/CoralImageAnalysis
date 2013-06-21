import numpy
import cv2
from matplotlib import pyplot as plt

'''A class with several different ways to normalize an image'''

def Tyler(img):
    '''
    Tyler's approach to normalizing an image.
    In this approach, we set each pixel to be 255 * the fraction of RGB at that pixel, thus we normalize the intensity.
    In reality we just pull out the things that are either almost all red, green, or blue, and the rest are set to nearly black
    '''

    if (len(img.shape) < 3):
        sys.stderr.write("For tyler normalization we use the BGR image and not each channel")

    im2 = numpy.zeros_like(img)
    for j in range(img.shape[0]):
        for i in range(img.shape[1]):
            sumrgb = int(img[j,i][0]) + int(img[j,i][1]) + int(img[j,i][2])
            if sumrgb == 0:
                #print i, " ", j, " = ", sumrgb, " : ", img[j,i][0], " ", img[j,i][1], " ", img[j,i][2]
                im2[j,i] = [0,0,0]
            else:
                b = (img[j,i][0]/sumrgb)*255
                g = (img[j,i][1]/sumrgb)*255
                r = (img[j,i][2]/sumrgb)*255
                im2[j,i] = [b,g,r]

    return im2

def simpleNorm(img):
    '''A simple normalization to make the maximum value 255'''
    imgc=numpy.zeros_like(img)
    for i in range(img.shape[2]):
        imgc[:,:,i] = img[:,:,i] * 255.0/img[:,:,i].max()
    return imgc

def equalizeHistograms(img):
    '''Use histogram equalization on each of the channels to normalize the image.
This is only valid for grayscale images, so we will convert the image if necessary.'''
    gr = img
    if len(img.shape)==3:
        gr = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    return cv2.equalizeHist(gr)



