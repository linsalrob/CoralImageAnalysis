#meta analysis file to accompanny randomForest_rewrite.py
#it should be used to compare and find the differences in probability between the two probability files.
import argparse
import sys
import csv
import numpy
import time

fileName1 = sys.argv[1]
#fileName2 = sys.argv[2]
#print "Parsing "+fileName1+" and "+fileName2+"."

file1 = open(fileName1,"r")   #open file in readonly mode
#file2 = open(fileName2,"r")
data1 = numpy.genfromtxt(file1,dtype='str',delimiter="\t") 
#data2 = numpy.genfromtxt(file2,dtype='str',delimiter="\t") 
#classes = data1[0:]
#data1=data1[1:] #remove 1st row, header
#data2=data2[1:]

print data1
print data1.shape
#data1.reshape()
"""PROGRAM OUTLINE"""

#grab 1st file
#munge the first row off

#grab 2nd file
#munge the first row off

#compare them frame by frame taking abs. diff and storing in new ndarray

#write ndarray out.


