#test_imageio_unittest.py
#unittest class for ImageIO.py
import unittest
import sys
import cv
import cv2
import Pillow
sys.path.append('../Modules/')
import ImageIO

class TestImageIO(unittest.TestCase):
    
    def setUp(self):
        self.imageFile = '../test/test.jpg'
        
    def test_cvread(self):
        img = ImageIO.cvread(self.imageFile)
        tmpImg = cv.LoadImage(self.imageFile)
        
        
        #equalityBool 
        #equalityBool = img == tmpImg
        #self.assertTrue(equalityBool)
    
    def test_as_array(self):
        pass
    
    def test_cv2read(self):
        pass
    
    def test_cv2grayscale(self):
        pass

if __name__=="__main__":
    unittest.main()