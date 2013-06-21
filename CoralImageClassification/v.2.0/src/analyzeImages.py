import sys
sys.path.append('../Modules/')
import os
import ImageIO
import Normalization
from Analysis import *
import argparse
import cv2


'''

A program to read a directory of files and calculate a bunch of statistics on those files.

We will print out the statistics and if we are given the details about the classification of
the image we will print that out too.

'''

parser = argparse.ArgumentParser(description='Analyze a series of images.')
parser.add_argument('-d', '--directory', help='The directory of images to analyse', required=True)
parser.add_argument('-f', '--file', help='File of images and their classifications')
parser.add_argument('-a', '--all', help='Process all files (otherwise only those in the classification file are processed). If no file is given, this is assumed', action='store_true')
args = parser.parse_args()

if not args.file:
    args.all = True

# define our analysis methods

# The stats class has min(), median(), mean(), max()
stats = Stats()

# The FFT class has energy()
fft = FFT()

# Edges has CAnny
edge = Edges()


classification = {}
if args.file:
    fin = open(args.file)
    for line in fin:
        line = line.rstrip()
        l = line.split("\t")
        if l[-1] != '-':
            classification[l[0]] = l[-1]


print ('\t'.join(map(str, ["Image File", "Classification", 
       "grayMin", "grayMax", "grayMedian", "grayMean", 
       "grayNormalizedMin", "grayNormalizedMax", "grayNormalizedMedian", "grayNormalizedMean", 
       "blueMin", "blueMax", "blueMedian", "blueMean", 
       "greenMin", "greenMax", "greenMedian", "greenMean", 
       "redMin", "redMax", "redMedian", "redMean", 
       "FFT",
       "Edge length"])))

images = os.listdir(args.directory)
for imgfile in images:
    if not args.all and imgfile not in classification:
        continue
    print imgfile, "\t",
    if imgfile in classification:
        print classification[imgfile], "\t",
    else:
        print "\t",

    img = ImageIO.cv2read(os.path.join(args.directory, imgfile))
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    print ('\t'.join(map(str, [stats.min(gray), stats.max(gray), stats.median(gray), stats.mean(gray)]))), "\t",
    
    gray = Normalization.equalizeHistograms(gray)
    print ('\t'.join(map(str, [stats.min(gray), stats.max(gray), stats.median(gray), stats.mean(gray)]))), "\t",

    for i in range(3):
        imp = img[:,:,i]
        print ('\t'.join(map(str, [stats.min(imp), stats.max(imp), stats.median(imp), stats.mean(imp)]))), "\t",
    print fft.energy(gray), "\t",  edge.sumCanny(gray)

