#Test file for Contours.py class
import sys
import numpy
import cv2
import unittest

sys.path.append('./Modules/')
from Contours import contours
import ImageIO

class TestContours(unittest.TestCase):
    
    def setUp(self):
        imageFile = './test/test.jpg'
        self.img = ImageIO.cv2read(imageFile)
        self.contours = contours(self.img)
    
    def test_withCanny_vs_raw_calculation(self):
        """!!!NOTE:
        I revisited this method on 06/23/14, I think I have the correct implementation.
        I fiddled with iteration of the 'list' of 'ndarray's which form the contour variables.
        I also converted the 'tmpImg' to grayscale, which was the source of earlier errors.
        """
        thresh1 = 1
        thresh2 = 255
        self.contours.withCanny(thresh1,thresh2)
        tmpImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        can = cv2.Canny(tmpImg,thresh1,thresh2)
        tmpContours,tmpHierarchy = cv2.findContours(can, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        boolList = ([]);
        
        #iterates over the two lists, which are composed of ndarrays.
        #This could probably be more efficient, I will have to do more research.
        for i in xrange(len(self.contours.contours)):
            boolList.append(numpy.all(self.contours.contours[i] == tmpContours[i]))
        
        contourBool = numpy.all(boolList)
        hierarchyBool = (self.contours.hierarchy == tmpHierarchy).all()
        self.assertTrue(contourBool and hierarchyBool)
        
    def test_numberOfCountours_vs_raw_calculation(self):
        con = self.contours.numberOfContours()
        thresh1 = 1
        thresh2 = 255
        tmpImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        tmpCan = cv2.Canny(tmpImg, thresh1, thresh2)
        tmpConts, tmpHierarchy = cv2.findContours(tmpCan, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.assertEqual(len(tmpConts),con)
    
    def test_numberOfClosedCountours_vs_raw_calculation(self):
        con = self.contours.numberOfClosedContours()
        thresh1 = 1
        thresh2 = 255
        tmpImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        tmpCan = cv2.Canny(tmpImg, thresh1, thresh2)
        tmpConts, tmpHierarchy = cv2.findContours(tmpCan, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        count = 0
        for c in tmpConts:
            if cv2.isContourConvex(c):
                count+=1
        self.assertEqual(con,count)
        
    def test_numberOfClosedContours_vs_raw_calculation(self):
        numCon = self.contours.numberOfOpenContours()
        thresh1 = 1
        thresh2 = 255
        tmpImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        tmpCan = cv2.Canny(tmpImg, thresh1, thresh2)
        tmpConts, tmpHierarchy = cv2.findContours(tmpCan, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        count = 0
        for c in tmpConts:
            if cv2.isContourConvex(c):
                count+=1
        tmpNumCon = len(tmpConts)
        convexCons = tmpNumCon - count
        self.assertEqual(convexCons,numCon)
        
    def test_numberOfConvexContours(self):
        """This is tested above, in 'test_numberOfClosedContours()'."""
    
    def test_numberOfConcaveContours(self):
        """This is tested above, in 'test_numberOfOpenContours()'."""
    
    def test_totalContourArea_vs_raw_calculation(self):
        conArea = self.contours.totalContourArea()
        thresh1 = 1
        thresh2 = 255
        tmpImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        tmpCan = cv2.Canny(tmpImg, thresh1, thresh2)
        tmpConts, tmpHierarchy = cv2.findContours(tmpCan, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        tmpArea = 0
        for c in tmpConts:
            tmpArea += cv2.contourArea(c)
        self.assertEqual(conArea,tmpArea)
        
    
    def test_largestContourByArea_vs__raw_calculation(self):
        conMax = self.contours.largestContourByArea()
        thresh1 = 1
        thresh2 = 255
        tmpImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        tmpCan = cv2.Canny(tmpImg, thresh1, thresh2)
        tmpConts, tmpHierarchy = cv2.findContours(tmpCan, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        tmpMax = None
        tmpMaxSize = 0
        for c in tmpConts:
            if cv2.contourArea(c) > tmpMaxSize:
                tmpMaxSize = cv2.contourArea(c)
                tmpMax = c
        equalityBool = (conMax == tmpMax).all()
        self.assertTrue(equalityBool)
    
    def test_showOnImage(self):
        thresh1 = 1
        thresh2 = 255
        self.contours.withCanny(thresh1,thresh2)
        conImage = self.contours.showOnImage(self.img,1,False)
        
        tmpImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        tmpCan = cv2.Canny(tmpImg, thresh1, thresh2)
        tmpConts, tmpHierarchy = cv2.findContours(tmpCan, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        tmpMax = None
        tmpMaxSize = 0
        
        tmpThickness = 1
        tmpImc = numpy.copy(self.img)
        for i in range(len(tmpConts)):
            #c1 = np.random.randint(255)
            #c2 = np.random.randint(255)
            #c3 = np.random.randint(255)
            c1 = 0
            c2 = 255
            c3 = 0
            cv2.drawContours(tmpImc,tmpConts, i, (c1,c2,c3),tmpThickness)
        #cv2.imshow('conImage',conImage)
        #cv2.waitKey(0)
        #cv2.imshow('tmpImc',tmpImc)
        #cv2.waitKey(0)
        equalityBool = (conImage == tmpImc).all()
        self.assertTrue(equalityBool)

    def test_totalPerimeterLength_vs_raw_calculation(self):
        length = self.contours.totalPerimeterLength()
        thresh1 = 1
        thresh2 = 255
        tmpImg = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        tmpCan = cv2.Canny(tmpImg, thresh1, thresh2)
        tmpConts, tmpHierarchy = cv2.findContours(tmpCan, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        tmpLen = 0
        for c in tmpConts:
            tmpLen += cv2.arcLength(c,cv2.isContourConvex(c))
        self.assertEqual(length,tmpLen)
    
    def test_findLines_vs_raw_calculation(self):
        lines = self.contours.findLines()
        image = self.img
        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        thresh1 = 1
        thresh2 = 255
        tmpCanny = cv2.Canny(image,thresh1,thresh2)
        tmpContours, tmpHierarchy = cv2.findContours(tmpCanny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        tmpLines = cv2.HoughLinesP(tmpCanny, 1, numpy.pi/180, 40, minLineLength=5)
        
        equalityBool = (lines == tmpLines).all()
        self.assertTrue(equalityBool)

    def test_lineLengths_vs_raw_calculation(self):
        length = self.contours.linelengths()
        
        image = self.img
        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        thresh1 = 1
        thresh2 = 255
        tmpCanny = cv2.Canny(image,thresh1,thresh2)
        tmpContours, tmpHierarchy = cv2.findContours(tmpCanny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        tmpLines = cv2.HoughLinesP(tmpCanny, 1, numpy.pi/180, 40, minLineLength=5)
        
        tmpLength = numpy.array([])
        lengtharr=[]
        for xy in tmpLines[0]:
            xyv = xy.reshape(2,2)
            inLength = numpy.linalg.norm(xyv[0]-xyv[1])
            lengtharr.append(inLength)

        tmpLength = numpy.array(lengtharr)
        equalityBool = (length == tmpLength).all()
        self.assertTrue(equalityBool)
    
    def test_medianLineLength_vs_raw_calculation(self):
        length = self.contours.linelengths()
        
        image = self.img
        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        thresh1 = 1
        thresh2 = 255
        tmpCanny = cv2.Canny(image,thresh1,thresh2)
        tmpContours, tmpHierarchy = cv2.findContours(tmpCanny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        tmpLines = cv2.HoughLinesP(tmpCanny, 1, numpy.pi/180, 40, minLineLength=5)
        
        tmpLength = numpy.array([])
        lengtharr=[]
        for xy in tmpLines[0]:
            xyv = xy.reshape(2,2)
            inLength = numpy.linalg.norm(xyv[0]-xyv[1])
            lengtharr.append(inLength)

        tmpLength = numpy.array(lengtharr)
        
        median = self.contours.medianLineLength()
        tmpMedian = numpy.median(tmpLength)
        self.assertEqual(median,tmpMedian)
    
    
    def test_meanLineLength_vs_raw_calculation(self):
        length = self.contours.linelengths()
        
        image = self.img
        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        thresh1 = 1
        thresh2 = 255
        tmpCanny = cv2.Canny(image,thresh1,thresh2)
        tmpContours, tmpHierarchy = cv2.findContours(tmpCanny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        tmpLines = cv2.HoughLinesP(tmpCanny, 1, numpy.pi/180, 40, minLineLength=5)
        
        tmpLength = numpy.array([])
        lengtharr=[]
        for xy in tmpLines[0]:
            xyv = xy.reshape(2,2)
            inLength = numpy.linalg.norm(xyv[0]-xyv[1])
            lengtharr.append(inLength)
        tmpLength = numpy.array(lengtharr)
        
        mean = self.contours.meanLineLength()
        tmpMean = numpy.mean(tmpLength)
        self.assertEqual(mean,tmpMean)
        
    
    def test_modeLineLength_vs_raw_calculation(self):
        length = self.contours.linelengths()
        
        image = self.img
        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        thresh1 = 1
        thresh2 = 255
        tmpCanny = cv2.Canny(image,thresh1,thresh2)
        tmpContours, tmpHierarchy = cv2.findContours(tmpCanny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        tmpLines = cv2.HoughLinesP(tmpCanny, 1, numpy.pi/180, 40, minLineLength=5)
        
        tmpLength = numpy.array([])
        lengtharr=[]
        for xy in tmpLines[0]:
            xyv = xy.reshape(2,2)
            inLength = numpy.linalg.norm(xyv[0]-xyv[1])
            lengtharr.append(inLength)
        tmpLength = numpy.array(lengtharr)
        
        mode = self.contours.modeLineLength()
        ints = numpy.rint(tmpLength).astype(int)
        counts = numpy.bincount(ints)
        tmpMode = numpy.argmax(counts)
        self.assertEqual(mode,tmpMode)
    
    def test_maxLineLength_vs_raw_calculation(self):
        length = self.contours.linelengths()
        
        image = self.img
        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        thresh1 = 1
        thresh2 = 255
        tmpCanny = cv2.Canny(image,thresh1,thresh2)
        tmpContours, tmpHierarchy = cv2.findContours(tmpCanny, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        tmpLines = cv2.HoughLinesP(tmpCanny, 1, numpy.pi/180, 40, minLineLength=5)
        
        tmpLength = numpy.array([])
        lengtharr=[]
        for xy in tmpLines[0]:
            xyv = xy.reshape(2,2)
            inLength = numpy.linalg.norm(xyv[0]-xyv[1])
            lengtharr.append(inLength)
        tmpLength = numpy.array(lengtharr)
        
        origMax = self.contours.maxLineLength()
        tmpMax = numpy.max(tmpLength)
        
        self.assertEqual(origMax,tmpMax)
    
if __name__=="__main__":
    unittest.main()