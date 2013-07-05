'''
A python class to handle the detection, highlighting, and closure of contours.

I wrote this as a separate class, because we need it for the ARMs plates analysis.

Rob E. 6/22/2013
'''

import cv2
import numpy

class contours:
    '''A class to detect contours in different ways'''

    def __init__(self, image):
        if len(image.shape) > 2:
            self.image=cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        else:
            self.image=image
        self.can = None
        self.contours = None
        self.hierarchy = None
        self.lines = None
        self.linelen = numpy.array([])

    def withCanny(self, threshold1=1, threshold2=255):
        '''Use Canny edge detection to find the contours in an image.'''
        # detect the edges with Canny edge detection
        self.can = cv2.Canny(self.image, threshold1, threshold2)
        # extract the contours and the hierarcy of those contours
        # The second argument can be one of:
        #     RETR_EXTERNAL retrieves only the extreme outer contours; It will set hierarchy[i][2]=hierarchy[i][3]=-1 for all the contours
        #     RETR_LIST retrieves all of the contours without establishing any hierarchical relationships
        #     RETR_CCOMP retrieves all of the contours and organizes them into a two-level hierarchy: on the top level are the external boundaries of the components, on the second level are the boundaries of the holes. If inside a hole of a connected component there is another contour, it will still be put on the top level
        #     RETR_TREE retrieves all of the contours and reconstructs the full hierarchy of nested contours. This full hierarchy is built and shown in OpenCV contours.c demo
        # The third argument can be one of:
        #     CHAIN_APPROX_NONE stores absolutely all the contour points
        #     CHAIN_APPROX_SIMPLE compresses horizontal, vertical, and diagonal segments and leaves only their end points. E.g. an up-right rectangular contour will be encoded with 4 points
        #     CHAIN_APPROX_TC89_L1 or CV_CHAIN_APPROX_TC89_KCOS
        ## self.contours, self.hierarchy = cv2.findContours(self.can, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        self.contours, self.hierarchy = cv2.findContours(self.can, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    def numberOfContours(self):
        '''The number of contours in the image'''
        if self.contours == None:
            self.withCanny()
        return len(self.contours)

    def numberOfClosedContours(self):
        '''The number of closed contours (i.e. make a circle like an O).
        Note: this is just an alias for numberOfConvexContours.'''
        return self.numberOfConvexContours()

    def numberOfOpenContours(self):
        '''The number of open contours (i.e. are like a C).
        Note: this is just an alias for numberOfConcaveContours.'''
        return self.numberOfConcaveContours()

    def numberOfConvexContours(self):
        '''The number of convex contours (i.e. make a circle like an O)'''
        if self.contours == None:
            self.withCanny()
        convex=0
        for c in self.contours:
            if cv2.isContourConvex(c):
                convex += 1
        return convex

    def numberOfConcaveContours(self):
        '''The number of concave contours (i.e. are like a C)'''
        if self.contours == None:
            self.withCanny()
        return self.numberOfContours() - self.numberOfConvexContours()

    def totalContourArea(self):
        '''Total area bounded by the contours'''
        if self.contours == None:
            self.withCanny()
        area=0
        for c in self.contours:
            area += cv2.contourArea(c)
        return area

    def largestContourByArea(self):
        '''Get the largest contour in the image, as defined by the area it bounds.'''
        if self.contours == None:
            self.withCanny()
        largest = None
        largestArea = 0
        for c in self.contours:
            if cv2.contourArea(c) > largestArea:
                largestArea = cv2.contourArea(c)
                largest = c
        return largest

    def showOnImage(self, im, thickness=1, fill=False):
        '''
        Display the contours on a COPY of an image. 
        The contours are displayed with random colors.
        The line thickness defaults to 1.
        You can choose to fill the contours too.
        '''
        if fill:
            thickness=-1

        imc=numpy.copy(im)
        for i in range(len(self.contours)):
            c1=numpy.random.randint(255)
            c2=numpy.random.randint(255)
            c3=numpy.random.randint(255)
            cv2.drawContours(imc, self.contours, i, (c1,c2,c3), thickness)
        return imc

    def totalPerimeterLength(self):
        '''
        Return the total length of perimeter of all the contours detected.
        '''
        if self.contours == None:
            self.withCanny()

        length=0
        for c in self.contours:
            length += cv2.arcLength(c, cv2.isContourConvex(c))

        return length


    def findLines(self):
        '''Find the lines associated with an image. 
        Returns an array of array's of X1,Y1,X2,Y2 legths.
        This will most likely be used as an internal method.'''
        if self.can == None:
            self.withCanny()
        self.lines = cv2.HoughLinesP(self.can, 1, numpy.pi/180, 40, minLineLength=5)
        return self.lines

    def linelengths(self):
        '''Return an array of line lengths for all the lines detected by the Hough transform.'''
        if self.lines == None:
            self.findLines()

        lengtharr=[]
        for xy in self.lines[0]:
            xyv = xy.reshape(2,2)
            length = numpy.linalg.norm(xyv[0]-xyv[1])
            lengtharr.append(length)

        self.linelen = numpy.array(lengtharr)
        return self.linelen

    def medianLineLength(self):
        '''Return the median line length for all the lines in the image'''
        if len(self.linelen) == 0: return 0
        return numpy.median(self.linelen)

    def meanLineLength(self):
        '''Return the mean line length for all the lines in the image'''
        if len(self.linelen) == 0: return 0
        return numpy.mean(self.linelen)


    def modeLineLength(self):
        '''Return the modal line length for all the lines in the image'''
        if len(self.linelen) == 0: return 0
        ints = numpy.rint(self.linelen).astype(int)
        counts = numpy.bincount(ints)
        return numpy.argmax(counts)

    def maxLineLength(self):
        '''Return the modal line length for all the lines in the image'''
        if len(self.linelen) == 0: return 0
        return numpy.max(self.linelen)




