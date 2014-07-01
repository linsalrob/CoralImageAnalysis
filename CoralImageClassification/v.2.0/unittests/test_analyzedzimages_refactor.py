#Test file for analyzeDZImages_Refactor.py classes

import sys
import unittest
sys.path.append('../src/')
import analyzeDZImages_Refactor as adz
sys.path.append('../Modules/')
import os
import ImageIO
import Normalization
from Analysis import *
import argparse
import cv2
import Classification
import Contours

class TestAnalysis(unittest.TestCase):
    
    def setUp(self):  
        pass
        
    def test_argProcessor(self):
        self.skipTest("Not implemented yet.")
        pass
        
    def test_moduleInitializer(self):
        modules = adz.moduleInitializer()
        tmpModules = [
            Stats(),
            FFT(),
            Laplacian(),
            Edges(),
            Features()]
            
        EqualityBool = True
        for i in xrange(len(modules)):
            if(type(modules.pop) != type(tmpModules.pop)):
                EqualityBool = False
                break
        self.assertTrue(EqualityBool)
        #self.assertEqual(tmpModules,modules)
    
    

if __name__ == '__main__':
	unittest.main()