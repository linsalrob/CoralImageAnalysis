#Python rewrite of randomForestTrainPredict.r for Coral Reef Classification project
#Uses scikit python module
import argparse
import sys
sys.path.append('../Modules/')
import munger
import csv
import numpy
import time
from sklearn.ensemble import RandomForestClassifier

infile = sys.argv[1]
print "Parsing "+infile+"."

file = open(infile,"r")   #open file in readonly mode
data = numpy.genfromtxt(file,dtype='str',delimiter="\t") #strips data out of file, and creates ndarray of strings

data = munger.deleteLastCol(data) #this is equal to data <- data[,1:(ncol(data)-1)]

