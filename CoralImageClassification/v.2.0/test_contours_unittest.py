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
    
    def test_withCanny(self):
        thresh1 = 1
        thresh2 = 255
        self.contours.withCanny(thresh1,thresh2)
        can = cv2.Canny(self.img,thresh1,thresh2)
        tmpContours,tmpHierarchy = cv2.findContours(can, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.assertListEqual(self.contours.contours, tmpContours)
        print type(self.contours.contours)
        print type(tmpContours)
        hierarchyBool = (self.contours.hierarchy == tmpHierarchy)
        self.assertTrue(contourBool)
        self.assertTrue(hierarchyBool)
        #self.assertTrue(contourBool and hierarchyBool)
        #tmpBool = (lapCalc==tmpLapCalc).all()
        
        
        #self.AssertEqual(,)
        #self.skipTest("Not implemented yet.")
    
    def test_numberOfCountours(self):
        self.skipTest("Not implemented yet.")
    
    def test_numberOfClosedCountours(self):
        self.skipTest("Not implemented yet.")
    
    def test_numberOfClosedContours(self):
        self.skipTest("Not implemented yet.")
    
    def test_numberOfConvexContours(self):
        self.skipTest("Not implemented yet.")
    
    def test_numberOfConcaveContours(self):
        self.skipTest("Not implemented yet.")
    
    def test_totalContourArea(self):
        self.skipTest("Not implemented yet.")
    
    def test_largestContourByArea(self):
        self.skipTest("Not implemented yet.")
    
    def test_showOnImage(self):
        self.skipTest("Not implemented yet.")
    
    def test_totalPerimeterLength(self):
        self.skipTest("Not implemented yet.")
    
    def test_findLines(self):
        self.skipTest("Not implemented yet.")
    
    def test_lineLengths(self):
        self.skipTest("Not implemented yet.")
    
    def test_medianLineLength(self):
        self.skipTest("Not implemented yet.")
    
    def test_meanLineLength(self):
        self.skipTest("Not implemented yet.")
    
    def test_modeLineLength(self):
        self.skipTest("Not implemented yet.")
    
    def test_maxLineLength(self):
        self.skipTest("Not implemented yet.")
    
if __name__=="__main__":
    unittest.main()