import cv
import cv2
import os
import numpy
from PIL import Image
from numpy import array


'''
Read and write images using openCV. This is a central class to read and write files and is really just a simple wrapper class. You don't need this at all!

'''


def cvread(filename):
    '''Use openCV to read an image'''
    return cv.LoadImage(filename)

def as_array(filename):
    '''Read an image using PIL and return it as a numpy array.
    Note you should probably use cv2read for this now.'''
    return  array(Image.open(os.path.join(source, toreg)), 'float64')


def cv2read(filename):
    '''Use cv2 to read an image'''
    return cv2.imread(filename)

def cv2grayscale(filename):
    '''Read an image and return the grayscale component'''
    im = cv2.imread(filename)
    grey = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    return grey



