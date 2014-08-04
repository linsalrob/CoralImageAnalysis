#crossTest.py
#rewrite of crossTest.r
import sys
sys.path.append('../Modules/')
import munger
import argparse
import csv
import numpy
import time
import cPickle  
import pickle
from sklearn.ensemble import RandomForestClassifier

#names = ["EKC.data.txt", "ELH1.data.txt", "ELH2.data.txt", "LHM5.data.txt", "NKH.data.txt", "WLH1.data.txt", "WLH2.data.txt", "all.txt", "all_not_EKC.txt", "all_not_ELH2.txt", "all_not_NKH.txt", "all_not_WLH2.txt", "all_not_ELH1.txt", "all_not_LHM5.txt", "all_not_WLH1.txt"]
#onames = ["EKC.data.txt", "ELH1.data.txt", "ELH2.data.txt", "LHM5.data.txt", "NKH.data.txt", "WLH1.data.txt", "WLH2.data.txt", "all.txt", "all_not_EKC.txt", "all_not_ELH2.txt", "all_not_NKH.txt", "all_not_WLH2.txt", "all_not_ELH1.txt", "all_not_LHM5.txt", "all_not_WLH1.txt"]

#These names are adjusted to remove references to the 'all_not' data.
#I could not find any 'all_not' files in any resources I have access to.

#I checked against the files which are produced from a 'sucessful run' of the program, and it does not generate data for the EKC or NKH data sets.
# removed the "EKC.data.txt" and "NKH.data.txt" accordingly.

#names = ["ELH1.data.txt", "ELH2.data.txt", "LHM5.data.txt", "WLH1.data.txt", "WLH2.data.txt", "all.txt"]
#onames = ["ELH1.data.txt", "ELH2.data.txt", "LHM5.data.txt", "WLH1.data.txt", "WLH2.data.txt", "all.txt"]

#For testing in src_refactor, names have been abbreviated to one case.
names=["ELH2.all.features.txt"]
onames=["ELH2.all.features.txt"]

for name in names:
    rffile = "rf/"+name+".rf.bin"
    with open(rffile,"rb") as f:
        forest = cPickle.load(f)
        
    #forestData = open(rffile,'rb')
    #forest=pickle.load(forestData)
    #print forest
    
    for oname in onames:
        fileName = oname
        print "Comparing "+name+".rf.bin"+" and "+oname
        file = open(fileName,"r")   #open file in readonly mode
        data = numpy.genfromtxt(file,dtype='str',delimiter="\t") #strips data out of file, and creates ndarray of strings
        #skipped na.omit(data) equivalent here, I don't believe this check is needed.
        #may need data munging here to get it to fit into the forest nicely
        p = forest.predict_proba(data)
        classes = forest.classes_
        namedp=numpy.vstack((classes,p))
        #classes = numpy.hstack(("Image File",classes))
        outtext = oname+"_data."+name+"_rf.probabilities.txt"
        outfile = open(outtext,"w")
        numpy.savetxt(outfile,namedp,fmt="%s",delimiter="\t",newline="\n")
        outfile.close()