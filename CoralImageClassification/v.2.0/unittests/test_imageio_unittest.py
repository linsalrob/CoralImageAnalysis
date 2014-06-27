#test_imageio_unittest.py
#unittest class for ImageIO.py
import unittest
import sys
import cv
import cv2
import numpy

#import Pillow
sys.path.append('../Modules/')
import ImageIO

class TestImageIO(unittest.TestCase):
    
    def setUp(self):
        self.imageFile = '../test/test.jpg'
        
    def test_cvread(self):
        img = ImageIO.cvread(self.imageFile)
        tmpImg = cv.LoadImage(self.imageFile)
        cv.AbsDiff(img,tmpImg,img)
  
        mat = cv.GetMat(img)
        arr = numpy.asarray(mat)
        
        equalityBool = (arr.all() == 0)
        self.assertTrue(equalityBool)
    
    def test_as_array(self):
        """This method is broken and will not run.
        The as_array method attempts to use the argument 'source' which is undefined.
        The notes state that cv2read should be used instead."""
        #img = ImageIO.as_array(self.imageFile)
        self.skipTest("Not implemented yet.")
    
    def test_cv2read(self):
        img = ImageIO.cv2read(self.imageFile)
        tmpImg = cv2.imread(self.imageFile)
        
        equalityBool = (img == tmpImg).all()
        self.assertTrue(equalityBool)
    
    def test_cv2grayscale(self):
        imgGray = ImageIO.cv2grayscale(self.imageFile)
        tmpImgGray = cv2.imread(self.imageFile)
        tmpImgGray = cv2.cvtColor(tmpImgGray,cv2.COLOR_BGR2GRAY)
        equalityBool = (imgGray == tmpImgGray).all()
        self.assertTrue(equalityBool)

if __name__=="__main__":
    unittest.main()