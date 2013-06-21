import numpy
import cv2
import sys

'''
A module that contains several different classes for the analysis of images.

Stats has some basic statistics, FFT has fast Fourier transform methods, Features is supposed to do feature detection (but see below), and edges has edge detection methods.

Note: At the moment the feature detection does not work. It is flaky in python openCV ... it was working in the last version but not the curent one.

'''


class Stats:
    '''Simple statistics for an image, eg. mean, median, min, max'''

    def min(self, img):
        '''The minimum value in an image (probably 0!)'''
        return numpy.min(img)

    def median(self, img):
        '''The median value in an image'''
        return numpy.median(img)

    def mean(self, img):
        '''The mean value for the image'''
        return numpy.mean(img)

    def max(self, img):
        '''The maximum value for the image (probably 254)'''
        return numpy.max(img)




class FFT:

    '''A class to handle the fft calls for image analysis'''

    def fft(self, img):
        '''Calculate the fast Fourier transformation of an image. This requires a 2D image (e.g. greyscale or single color channel.
        fft = fft(img)
        '''
        if (len(img.shape) != 2):
            sys.stderr.write("The image passed to fft is not a 2D image. Please refactor")
            sys.exit(-1)

        return numpy.fft.fft2(img)

    def energy(self, img):
        '''The energy in the image is calculated as the square root of the sum of squares of the magnitude of the fft (the real part). 
        Returns a single integer for the image. '''

        return numpy.sqrt(numpy.sum(numpy.abs(self.fft(img)) ** 2))


class Features:
    '''An internal class to extract some information based on the number of keypoints in the image.

    We use SURF feature detection to extract the laplacian and the hessians of the image'''
    
    def __init__(self):
        self.img = None
        self.keypoints = None
        self.descarray = None
        self.lp = None
        self.he = None

    def detect_kp(self, img):
        '''Detect the keypoints in the image'''

        if (len(img.shape) != 2):
            sys.stderr.write("The image passed to SURFs is not a 2D image. Please refactor")
            sys.exit(-1)

        try:
            s = cv2.SURF()
        except:
            sys.stderr.write("WARNING: The current version of cv2 " + str(cv2.__version__)  + " does not appear to contain SURF(). This is a bit flaky, so try again in a bit!\n\n")
            return

        self.img = img
        s = cv2.SURF()
        self.keypoints, self.descarray = s.detect(grey, None, useProvidedKeypoints = False)
        self.lp = round(keypoints.class_id)
        self.he = keypoints.response

    def laplacian(self, img):
        if self.img != img:
            sys.stderr.write("Redetecting features\n")
            self.detect_kp(img)
        return self.lp

    def hessian(self, img):
        if self.img != img:
            sys.stderr.write("Redetecting features\n")
            self.detect_kp(img)
        return self.he


class Edges:
    '''Various edge detection techniques'''

    def Canny(self, img, threshold1=1, threshold2=255):
        '''Canny edge detection with two thresholds to find the edges between'''
        return cv2.Canny(img, threshold1, threshold2)

    def sumCanny(self, img, threshold1=1, threshold2=255):
        '''The total length of the edges in the image'''
        return numpy.sum(self.Canny(img, threshold1, threshold2))

