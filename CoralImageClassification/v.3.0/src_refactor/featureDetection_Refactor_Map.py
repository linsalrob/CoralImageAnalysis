#featureDetection_Refactor_Map.py

import sys
sys.path.append('../Modules/')
import os
import ImageIO
import Normalization
from Analysis import *
import argparse
from multiprocessing import Pool
import time as t

def argProcessor():
    parser = argparse.ArgumentParser(description='Analyze a series of images.')
    parser.add_argument('-d', '--directory', help='The directory of images to analyse', required=True)
    parser.add_argument('-o', '--output', help='The output file. If this file exists, images in the file will be skipped and the file will be appended', required=True)
    parser.add_argument('-v', '--verbose', help='Verbose output', action='store_true')
    args = parser.parse_args()
    return args
    
def outputPreperationHandler():
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
        fout.write( ('\t'.join(map(str, ["Image File", "NumberKeyPoints", "MedianKPSize", "MeanKPSize"]))) +"\t")
        for i in range(15):
            fout.write( "KPsOver" + str(10*i) + "\t")
        fout.write("\n")  
    return args,fout,seen
    
def imageHandler(imgfile):
    retStrings = []
    
    if imgfile in seen:
        return
    
    if os.path.isdir(os.path.join(args.directory, imgfile)):
        temp = os.listdir(os.path.join(args.directory, imgfile))
        for f in temp:
            images.append(os.path.join(imgfile, f))
        return
    
    # silently skip the bin files that have the gps data
    if imgfile.endswith('bin'):
        return
    # alert to other files that were skipped
    if not (imgfile.endswith('png') | imgfile.endswith('jpg')):
        sys.stderr.write("Skipped file: " + imgfile + "\n")
        return
    
    if args.verbose:
        sys.stderr.write("Parsing " + imgfile + "\n")
    
    retStrings.append( imgfile + "\t" )
    
    img = ImageIO.cv2read(os.path.join(args.directory, imgfile))
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ngray = Normalization.equalizeHistograms(gray)
    ngray = cv2.GaussianBlur(ngray, (3,3), 0)
    
    feats.detect_kp_ORB(ngray)
    retStrings.append( str(feats.numberKeyPoints()) + "\t" + str(feats.medianKeyPointSize()) + "\t" + str(feats.meanKeyPointSize()) )
    
    for i in range(15):
        retStrings.append("\t" + str(feats.numKeyPoints(i*10)))
    retStrings.append("\n")
    
    return retStrings

def testMain():
    global args
    args = argProcessor()
    global feats
    feats=Features()
    global fout
    fout=None;
    global seen
    seen={}
    args,fout,seen=outputPreperationHandler()
    global images
    images=os.listdir(args.directory)
    if'.DS_Store' in images: 
        images.remove('.DS_Store') #causes errors if .DS_Store is not removed.
        
    imagesSubDirectories = []
    for directory in images:    
        fullDir = args.directory+"/"+directory #build full directory name
        tmpList = os.listdir(fullDir) #list out directory contents (files in subdirectories)
        for file in tmpList:
            imagesSubDirectories.append(directory+"/"+file)
    
    stringsToPrint=[]
    ret = []
    numProcesses = 16
    pool = Pool(numProcesses)
    ret = pool.map(imageHandler, imagesSubDirectories)  
    stringsToPrint.append(ret)
    pool.close()
    pool.join()
    
    fout=open(args.output, 'a')
    for run in stringsToPrint:
        for element in ret:
            if element != None:
                for string in element:
                    fout.write(string)
    
def mainFunc(): #original implementation
    #print "started!"
    args = argProcessor()
    feats=Features()
    fout=None;
    seen={}
    args,fout,seen=outputPreperationHandler(args,fout,seen)
    images=os.listdir(args.directory)
    imageHandler(args,fout,seen,feats,images)
    
if __name__ == '__main__':
	testMain()
    #mainFunc()