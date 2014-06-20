#Test file for Analysis.py classes
import sys
import numpy
import cv2

#import Image

import unittest
sys.path.append('./Modules/')
import Normalization
import ImageIO
from Analysis import Edges
from Analysis import Laplacian
from Analysis import Features
from Analysis import Stats as stats
from Analysis import FFT as fft

class TestAnalysis(unittest.TestCase):
    
    def setUp(self):  
        imageFile = './test/test.jpg'
        self.image = ImageIO.cv2read(imageFile)
        self.grayscale = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        self.stats = stats()
        self.fft = fft()
        self.feats = Features()
        self.lap = Laplacian()
        self.edges = Edges()
        
    """Stat class tests""" 
     
    def test_Stat_min_vs_image_min(self):
        self.assertEqual( self.stats.min(self.image), self.image.min() )
        #research if image.min() is a valid value to test against.
        
    def test_Stat_median_vs_image_median(self):
        #!!!Note: image is of type 'numpy.ndarray'
        self.assertEqual( self.stats.median(self.image), numpy.median(self.image) )
    
    def test_Stat_mean_vs_image_mean(self):
        self.assertEqual( self.stats.mean(self.image), self.image.mean() )
    
    def test_Stat_max_vs_image_max(self):
        self.assertEqual( self.stats.max(self.image), self.image.max() )
    
    
    """FFT class tests"""
    
    def test_FFT_fft_vs_raw_calculation(self):
        img = self.image
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ngray = Normalization.equalizeHistograms(gray)
        
        fftImage = self.fft.fft(ngray)
        
        tmpFftImage = numpy.fft.fft2(ngray)
        tmpBool = (fftImage==tmpFftImage).all()
        self.assertTrue(tmpBool)

    """
    def test_FFT_fft_vs_cv2_dft(self):    
        #img = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        #dft = cv2.dft(img,flags = cv2.DFT_COMPLEX_OUTPUT)
        #dft = cv2.dft(numpy.float32(img),flags = cv2.DFT_REAL_OUTPUT)
        #dft = 
        dft = cv2.dft(img)
        print type(img)
        print type(dft)
        dft_shift = numpy.fft.fftshift(dft)
        self.assertEqual( self.fft.fft(img), dft_shift )
        #self.assertEqual( self.fft.fft(img), cv2.dft(img) )
    """
        
    def test_FFT_energy_vs_cv2_raw_calculation(self):
        self.skipTest("Not implemented yet.")
        #I am not sure if open cv provides equivalent functionality
        #for now I think I should recalculate the value using my own function
        #pass
        pass
        
        
    """Features class tests"""    
    
    def test_Feature_detect_kp_surf_vs_raw_calculation(self):
        """!!!Note:
        The Features.detect_kp_surf() seems to have a serious problem
        The method uses a variable "grey", but this is not defined anywhere, and it not some kind of CV2 constant.
        upon trying to call detect_kp_surf() python throws an error "global name 'grey' is not defined".
        I haven't found this method used in actual code yet, so it may be dead code."""
        
        
        #img = self.image
        #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #s = cv2.SURF()
        #features = Features()
        #self.feats.detect_kp_surf(self.grayscale)
        #features.keypoints, features.descarray = s.detect(self.image,None, useProvidedKeypoints = False)
        #features.lp = round(keypoints.class_id)
        #features.he = keypoints.response
        
        self.skipTest("Not implemented yet.")
        pass
    
    def test_Features_detect_kp_ORB_vs_clean_class(self):
        img = self.image
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ngray = Normalization.equalizeHistograms(gray)
        
        kp_ORB = self.feats.detect_kp_ORB(ngray)
        
        tmpfeats = Features()
        tmp_kp_ORB = tmpfeats.detect_kp_ORB(ngray)
        self.assertEqual(kp_ORB,tmp_kp_ORB)
        
    def test_Features_detect_kp_ORB_vs_raw_calculation(self):
        img = self.image
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ngray = Normalization.equalizeHistograms(gray)
        self.feats.detect_kp_ORB(ngray)
        
        orbdetector = cv2.FeatureDetector_create('ORB')
        keypointsizes=[]
        keypoints = orbdetector.detect(ngray, None)
        for k in keypoints:
            keypointsizes.append(k.size)
        keypointsizes = numpy.array(keypointsizes)
    
        tmpBool = (self.feats.keypointsizes==keypointsizes).all()
        self.assertTrue(tmpBool)
        
    def test_Features_numberKeyPoints_vs_clean_class(self):
        img = self.image
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ngray = Normalization.equalizeHistograms(gray)
        
        kp_ORB = self.feats.detect_kp_ORB(ngray)
        tmpfeats = Features()
        tmpfeats.detect_kp_ORB(ngray)
        
        pts = self.feats.numberKeyPoints()
        tmpPts = tmpfeats.numberKeyPoints()
        self.assertEqual(pts,tmpPts)
    
    def test_Features_medianKeyPointSize_vs_clean_class(self):
        img = self.image
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ngray = Normalization.equalizeHistograms(gray)
        
        self.feats.detect_kp_ORB(ngray)
        median = self.feats.medianKeyPointSize()
        
        tmpfeats = Features()
        tmpfeats.detect_kp_ORB(ngray)
        tmpMedian = numpy.median(tmpfeats.keypointsizes)
        
        self.assertEqual(median,tmpMedian)
    
    def test_Features_meanKeyPointSize_vs_clean_class(self):
        img = self.image
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ngray = Normalization.equalizeHistograms(gray)
        
        self.feats.detect_kp_ORB(ngray)
        mean = self.feats.meanKeyPointSize()
        
        tmpfeats = Features()
        tmpfeats.detect_kp_ORB(ngray)
        tmpMean = numpy.mean(tmpfeats.keypointsizes)
        
        self.assertEqual(mean,tmpMean)
    
    def test_Features_numKeyPoints_vs_clean_class(self):
        img = self.image
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ngray = Normalization.equalizeHistograms(gray)
        
        self.feats.detect_kp_ORB(ngray)
        pts = self.feats.numKeyPoints()
        
        tmpfeats = Features()
        tmpfeats.detect_kp_ORB(ngray)
        tmpPts = sum(tmpfeats.keypointsizes > 50)

        self.assertEqual(pts,tmpPts)
        
    def test_Features_laplacian(self):
        """!!!Note:
        Upon executing any instance of Features.laplacian(), 
        if self.img does not equal the image passed to the function,
        the program will terminate because laplacian() calls self.detect_kp(img).
        This fails because Features has no method called detect_kp().
        """
        
        self.skipTest("Not implemented yet.")
        
        #img = self.image
        #gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        #ngray = Normalization.equalizeHistograms(gray)
        #self.feats.detect_kp_ORB(ngray)
        #lap = self.feats.laplacian(self.image)
        
        #tmpfeats = Features()
        #tmpfeats.detect_kp_ORB(ngray)
        
        #tmpLap = tmpfeats.laplacian(self.image)
        #assertEqual(lap,tmpLap)
        
    def test_Features_hessian(self):
        """!!!Note:
        Features.hessian() has the same error as the laplacian method.
        No, detect_kp() method in the code.
        Check test_Features_laplacian() for further details.
        """
        self.skipTest("Not implemented yet.")
        
        
        
    """Laplacian class tests""" 
    
    def test_Laplacian_calculate_vs_raw_calcuation(self):
        """!!!Note:
        This is a helper method called from within Laplacian.sum().
        """
        
        
        img = self.image
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ngray = Normalization.equalizeHistograms(gray)
        kern = 3
        
        lapCalc = self.lap.calculate(img,kern,)
        tmpLapCalc = cv2.Laplacian(gray,cv2.CV_16U,ksize=kern)

        tmpBool = (lapCalc==tmpLapCalc).all()
        self.assertTrue(tmpBool)
        
    def test_Laplacian_sum_vs_raw_calculation(self):
        img = self.image
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ngray = Normalization.equalizeHistograms(gray)
        kern = 9
        lapSum = self.lap.sum(ngray,kern)
        
        
        tmpLap = Laplacian()
        gl = tmpLap.calculate(ngray,kern,)
        glo = gl>10
        tmpLapSum = numpy.sum(glo)
        
        self.assertEqual(lapSum,tmpLapSum)
        
    """Edges class tests"""
    
    def test_Edges_Canny_vs_raw_calculation(self):
        """!!!Note:
        This is a helper method called within Edges.sumCanny().
        """
        img = self.image
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ngray = Normalization.equalizeHistograms(gray)
        cann = self.edges.Canny(ngray,1,255)
        
        tmpCann = cv2.Canny(ngray,1,255)
        
        tmpBool = (cann==tmpCann).all()
        self.assertTrue(tmpBool)
    
    def test_Edges_sumCanny_vs_raw_calculation(self):
        img = self.image
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ngray = Normalization.equalizeHistograms(gray)
        sumCann = self.edges.sumCanny(ngray,1,255)
        
        tmpCann = cv2.Canny(ngray,1,255)
        tmpSumCann = numpy.sum(tmpCann)
        
        self.assertEqual(tmpSumCann,sumCann)
        
    
if __name__ == '__main__':
	unittest.main()