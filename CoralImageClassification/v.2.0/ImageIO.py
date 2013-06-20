import cv
import cv2
import os
import numpy
from PIL import Image
from numpy import array


class ImageIO:
    '''Read and write images using openCV. This is a central class to read what we need'''

    def __init__(self):
        self.loaded = 1

    def cvread(self, filename):
        '''Use openCV to read an image'''
        return cv.LoadImage(filename)

    def as_array(self, filename):
        '''Read an image using PIL and return it as a numpy array.
        Note you should probably use cv2read for this now.'''
        return  array(Image.open(os.path.join(source, toreg)), 'float64')


    def cv2read(self, filename):
        '''Use cv2 to read an image'''
        return cv2.imread(filename)

    def cv2grayscale(self, filename):
        '''Read an image and return the grayscale component'''
        im = cv2.imread(filename)
        grey = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        return grey



