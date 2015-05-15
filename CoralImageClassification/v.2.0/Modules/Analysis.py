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

    We use SURF feature detection to extract the laplacian and the hessians of the image.

    NOTE: SURF is patented and you are supposed to pay for it. However, ORB is completely open and so it has replaced SURF in cv2.
    For more information see http://docs.opencv.org/trunk/doc/py_tutorials/py_feature2d/py_orb/py_orb.html'''
    
    def __init__(self):
        self.img = None
        self.keypoints = None
        self.descarray = None
        self.lp = None
        self.he = None
        self.keypointsizes=[]
        self.orbdetector = None
        self.keypoints = None

    def detect_kp_surf(self, img):
        '''Detect the keypoints in the image by SURF'''

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

    def detect_kp_ORB(self, img):
        ''' detect the keypoints by ORB algorithm''' 
        if (len(img.shape) != 2):
            sys.stderr.write("The image passed to SURFs is not a 2D image. Please refactor")
            sys.exit(-1)
        
        self.orbdetector = cv2.FeatureDetector_create('ORB')
        # change the number of features detected: self.orbdetector.setInt('nFeatures', 100)
        self.keypointsizes=[]
        self.keypoints = self.orbdetector.detect(img, None)
        for k in self.keypoints:
            self.keypointsizes.append(k.size)
        self.keypointsizes = numpy.array(self.keypointsizes)

    def numberKeyPoints(self):
        '''Get the number of keypoints'''
        return len(self.keypointsizes)

    def medianKeyPointSize(self):
        '''Get the median size of the keypoints'''
        return numpy.median(self.keypointsizes)

    def meanKeyPointSize(self):
        '''Get the mean size of the key points'''
        return numpy.mean(self.keypointsizes)

    def numKeyPoints(self, minSize=50):
        '''Get the number of key points larger than a give size (default: 50)'''
        return sum(self.keypointsizes > minSize)




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

class Laplacian:
    '''Calculate the Laplacian (2nd derivative) of the image.
    The kernel size must be an odd number between 1 and 31. 
    Seven or nine seem like good defaults.'''

    def calculate(self, img, kernel, ddepth=cv2.CV_16U):
        gray = img
        if len(img.shape) > 2:
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        return cv2.Laplacian(gray,ddepth,ksize = kernel)

    def sum(self, img, kernel=9):
        gl = self.calculate(img, kernel, cv2.CV_16U)
        # count the number of points > 1 (i.e. that are edges)
        ## RAE: 8/7/13: before this was 10?? glo = gl > 10
        glo = gl > 1
        # return the number of True points
        return numpy.sum(glo)

class Edges:
    '''Various edge detection techniques'''

    def Canny(self, img, threshold1=1, threshold2=255):
        '''Canny edge detection with two thresholds to find the edges between'''
        return cv2.Canny(img, threshold1, threshold2)

    def sumCanny(self, img, threshold1=1, threshold2=255):
        '''The total length of the edges in the image'''
        return numpy.sum(self.Canny(img, threshold1, threshold2))

