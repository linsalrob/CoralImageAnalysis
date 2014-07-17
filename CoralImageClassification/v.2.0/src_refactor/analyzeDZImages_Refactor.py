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

def classificationHandler(args):
    classification = {}
    if args.file:
        for f in args.file:
            sys.stderr.write("Parsing the classifications in " + f + "\n")
            """From Classification.py"""
            classifier = Classification.Parsers(f)
            newclass={}
            if args.tab:
                newclass = classifier.tab()
            else:
                newclass = classifier.zawada()
            for c in newclass:
                classification[c] = newclass[c]               
    return classification

def outputHandler(fout, seen, args):    
    if (os.path.exists(args.output)):
        # if the output exists we need to read it and collect all the files we have seen
        fout=open(args.output, 'r')
        for line in fout:
            pieces = line.split('\t')
            seen[pieces[0]]=1
        fout.close()
        fout=open(args.output, 'a')
    else:
        # if we have created a new output file we need to print the header. 
        # If we are appending to an existing output file we do not need to create the header
        fout=open(args.output, 'w')
        fout.write( ('\t'.join(map(str, ["Image File", "Classification", 
               "grayMin", "grayMax", "grayMedian", "grayMean", 
               "gnMin", "gnMax", "gnMedian", "gnMean", 
               "blueMin", "blueMax", "blueMedian", "blueMean", 
               "greenMin", "greenMax", "greenMedian", "greenMean", 
               "redMin", "redMax", "redMedian", "redMean", 
               "FFT", "nFFT", "NumKeyPoints", "MedianKPSize", "MeanKPSize"]))) +"\t")
    
        for i in range(15):
            fout.write( "KPsOver" + str(10*i) + "\t")

        for i in range(15):
            fout.write( "Lapl" + str(2*i+1) + "\t")

        for i in range(25):
            fout.write( "Can1." + str(10*i) + "\t")

        for i in range(5):
            t=50*i
            fout.write( "Contours" + str(t) + "\tClosedCont" + str(t) + "\tOpenCont" + str(t) + "\tContArea" + str(t) + "\tLargestCont" + str(t) + "\tPerimeter" + str(t) + "\t")
            fout.write( "MaxLL" + str(t) + "\tMeanLL" + str(t) + "\tMedianLL" + str(t) + "\tModeLL" + str(t) + "\t")

        fout.write("\n")
    return (fout,seen)
    
def imageWriter(images,seen,args,fout,classification,stats,fft,lap,edge):
    for imgfile in images:

        if imgfile in seen: continue

        if os.path.isdir(os.path.join(args.directory, imgfile)):
            temp = os.listdir(os.path.join(args.directory, imgfile))
            for f in temp:
                images.append(os.path.join(imgfile, f))
            continue

        if not args.all and imgfile not in classification:
            continue

        # silently skip the bin files that have the gps data
        if imgfile.endswith('bin'):
            continue
        # alert to other files that were skipped
        if not (imgfile.endswith('png') | imgfile.endswith('jpg')):
            sys.stderr.write("Skipped file: " + imgfile + "\n")
            continue

        if args.verbose:
            sys.stderr.write("Parsing " + imgfile + "\n")

        fout.write( imgfile + "\t" )
        if imgfile in classification:
            fout.write( classification[imgfile] + "\t")
        else:
            fout.write( "unknown\t" )

        img = ImageIO.cv2read(os.path.join(args.directory, imgfile))
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        fout.write( ('\t'.join(map(str, [stats.min(gray), stats.max(gray), stats.median(gray), stats.mean(gray)]))) + "\t" )

        ngray = Normalization.equalizeHistograms(gray)
        # apply a gaussian blur to remove edge effects
        ngray = cv2.GaussianBlur(ngray, (3,3), 0)
        fout.write( ('\t'.join(map(str, [stats.min(ngray), stats.max(ngray), stats.median(ngray), stats.mean(ngray)]))) + "\t")

        for i in range(3):
            imp = img[:,:,i]
            fout.write( ('\t'.join(map(str, [stats.min(imp), stats.max(imp), stats.median(imp), stats.mean(imp)]))) + "\t" )
        fout.write( str(fft.energy(gray)) + "\t" + str(fft.energy(ngray)) + "\t")

        if args.features:
            feats.detect_kp_ORB(ngray)
            fout.write( str(feats.numberKeyPoints()) + "\t" + str(feats.medianKeyPointSize()) + "\t" + str(feats.meanKeyPointSize()) + "\t")

            for i in range(15):
                fout.write( str(feats.numKeyPoints(i*10)) + "\t")
        else:
            fout.write("0\t0\t0\t");
            for i in range(15):
                fout.write("0\t")
    
        for i in range(15):
            k=2*i+1
            fout.write( str(lap.sum(ngray, k)) + "\t")

        for i in range(25):
            t2 = 10*i
            fout.write( str(edge.sumCanny(ngray, 1, t2)) + "\t")
        #edge.sumCanny(gray)

        # Contour detection
        ctr = Contours.contours(ngray)
        for i in range(5):
            threshold=50*i
            ctr.withCanny(1, threshold)
            if ctr.numberOfContours() == 0:
                fout.write( "0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" )
            else:
                try:
                    fout.write( "\t".join(map(str, [ctr.numberOfContours(), ctr.numberOfClosedContours(),
                                          ctr.numberOfOpenContours(), ctr.totalContourArea(), cv2.contourArea(ctr.largestContourByArea()),
                                          ctr.totalPerimeterLength()])) + "\t")
                    ctr.linelengths()
                    fout.write( "\t".join(map(str, [ctr.maxLineLength(), ctr.meanLineLength(), ctr.medianLineLength(), ctr.modeLineLength()])) + "\t")
                except Exception as e:
                    sys.stderr.write("There was an error calculating the contours for " + imgfile +": " + e.message + "\n")
                    fout.write( "0\t0\t0\t0\t0\t0\t0\t0\t0\t0\t" )

        fout.write("\n")    
    
def testMain():
    print "started!"
    args = argProcessor()
    if not args.file:
        args.all = True
    
    stats, fft, lap, edge, feats = (None,)*5
    modules = moduleInitializer()
    modules.reverse()
    stats = modules.pop()
    fft = modules.pop()
    lap = modules.pop()
    edge = modules.pop()
    feats = modules.pop()
    classification = classificationHandler(args)
    fout=None;
    seen={}
    fout, seen = outputHandler(fout,seen,args)
    print fout
    print seen
    images = os.listdir(args.directory)
    imageWriter(images,seen,args,fout,classification,stats,fft,lap,edge)
    
if __name__ == '__main__':
	testMain()