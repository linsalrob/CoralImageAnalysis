import sys
#sys.path.append('/Users/Tosti/Desktop/CS_Lab_Spring_14/CoralImageAnalysis/CoralImageClassification/v.2.0/Modules/')
sys.path.append('../Modules/')
import os
import ImageIO
import Normalization
from Analysis import *
import argparse
import cv2
import Classification
import Contours




def argProcessor():
    parser = argparse.ArgumentParser(description='Analyze a series of images.')
    parser.add_argument('-d', '--directory', help='The directory of images to analyse', required=True)
    parser.add_argument('-f', '--file', help='File of images and their classifications', action='append')
    parser.add_argument('-t', '--tab', help='Classification is tab separated text (default: Zawada format)')
    parser.add_argument('-a', '--all', help='Process all files (otherwise only those in the classification file are processed). If no file is given, this is assumed', action='store_true')
    parser.add_argument('-o', '--output', help='The output file. If this file exists, images in the file will be skipped and the file will be appended', required=True)
    parser.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
    parser.add_argument('-u', '--features', help='Include feature detection. Requires most modern openCV', action='store_true')
    args = parser.parse_args()
    return args
    
def moduleInitializer():
    modules = []
    # The stats class has min(), median(), mean(), max()
    """From Analysis.py"""
    stats = Stats()
    modules.append(stats)
    
    # The FFT class has energy()
    """From Analysis.py"""
    fft = FFT()
    modules.append(fft)
    # the Laplacian class calculates the laplacian
    """From Analysis.py"""
    lap = Laplacian() 
    modules.append(lap)

    # Edges has CAnny #Canny part of OpenCV module
    """From Analysis.py"""
    edge = Edges()
    modules.append(edge)

    # features for the  .. features 
    """From Analysis.py"""
    feats=Features()
    modules.append(feats)
    return modules

def tmpMain():
    print "started!"
    args = argProcessor()
    if not args.file:
        args.all = True
    stats = None
    fft = None
    lap = None
    edge = None
    feats = None
    modules = moduleInitializer()
    modules.reverse()
    stats = modules.pop()
    fft = modules.pop()
    lap = modules.pop()
    edge = modules.pop()
    feats = modules.pop()
    
    
        
#if __name__ == '__main__':
	#tmpMain()