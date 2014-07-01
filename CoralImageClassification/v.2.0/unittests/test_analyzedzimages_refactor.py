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
        
    def test_moduleInitializer_vs_raw_equivalent(self):
        modules = adz.moduleInitializer()
        tmpModules = [
            Stats(),
            FFT(),
            Laplacian(),
            Edges(),
            Features()]  
            
        EqualityBool = True
        for i in xrange(len(modules)):
            mod1 = modules[i].__class__.__name__
            mod2 = tmpModules[i].__class__.__name__
            if mod1 != mod2:
                EqualityBool = False
                break
        self.assertTrue(EqualityBool)
    
    def test_moduleInitializer_vs_self_reverse(self):
        modules = adz.moduleInitializer()
        tmpModules = adz.moduleInitializer()
        tmpModules.reverse()
            
        EqualityBool = True
        for i in xrange(len(modules)):
            mod1 = modules[i].__class__.__name__
            mod2 = tmpModules[i].__class__.__name__
            if mod1 != mod2:
                EqualityBool = False
                break
        self.assertFalse(EqualityBool)
    
    
    

if __name__ == '__main__':
	unittest.main()