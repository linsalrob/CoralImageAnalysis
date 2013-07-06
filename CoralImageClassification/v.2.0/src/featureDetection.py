import sys
sys.path.append('../Modules/')
import os
import ImageIO
import Normalization
from Analysis import *
import argparse

'''

A program to just calculate the feature size information for a range of images.


'''


parser = argparse.ArgumentParser(description='Analyze a series of images.')
parser.add_argument('-d', '--directory', help='The directory of images to analyse', required=True)
args = parser.parse_args()



