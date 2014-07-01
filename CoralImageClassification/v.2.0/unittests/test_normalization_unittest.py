#test_normalization_unittest.py
#unittest class for Normalization.py
import unittest
import sys
import numpy
import cv2
sys.path.append('../Modules/')
import Normalization
import ImageIO

class TestClassification(unittest.TestCase):
    
    def setUp(self):
        imageFile = '../test/test.jpg'
        self.img = ImageIO.cv2read(imageFile)
        
        
    def test_tyler(self):
        tylerImg = Normalization.Tyler(self.img)
        img = self.img
        im2 = numpy.zeros_like(img)
        for j in range(img.shape[0]):
            for i in range(img.shape[1]):
                sumrgb = int(img[j,i][0]) + int(img[j,i][1]) + int(img[j,i][2])
                if sumrgb == 0:
                    im2[j,i] = [0,0,0]
                else:
                    b = (int(img[j,i][0]/sumrgb)*255)
                    g = (int(img[j,i][1]/sumrgb)*255)
                    r = (int(img[j,i][2]/sumrgb)*255)
                    im2[j,i]=[b,g,r]
                    
        equalityBool = (tylerImg == im2).all()
        self.assertTrue(equalityBool)
    
    def test_simpleNorm(self):
        simpleNorm = Normalization.simpleNorm(self.img)
        
        img = self.img
        imgc = numpy.zeros_like(img)
        for i in range(img.shape[2]):
            imgc[:,:,i] = img[:,:,i] * 255.0/img[:,:,i].max()
        
        equalityBool = (simpleNorm == imgc).all()
        self.assertTrue(equalityBool)
    
    def test_equalizeHistograms(self):
        equalHist = Normalization.equalizeHistograms(self.img)
        
        img = self.img
        gr = img
        if len(img.shape)==3:
            gr = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        tmpEqualHist = cv2.equalizeHist(gr)
        equalityBool = (equalHist == tmpEqualHist).all()
        self.assertTrue(equalityBool)
    
if __name__=="__main__":
    unittest.main()