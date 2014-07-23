#randomForestPredictNoTrimProbabilityCompare.py
#meta analysis file to accompanny randomForestPredictNoTrim_rewrite.py
#it should be used to compare and find the differences in probability between the two probability files.
#from inside the 'src_refactor' folder use the folowing to run test
#python randomForestPredictNoTrimProbabilityCompare.py ../executionDir/probabilities/ELH2.all.features.txt.probabilities.txt ./probabilities/ELH2.all.features.txt.probabilities.txt
import argparse
import sys
import csv
import numpy
import time
import munger

fileName1 = sys.argv[1]
fileName2 = sys.argv[2]
print "Parsing "+fileName1+" and "+fileName2+"."

file1 = open(fileName1,"r")   #open file in readonly mode
file2 = open(fileName2,"r")

data1 = numpy.genfromtxt(file1,dtype='str',delimiter="\t",usecols=(1,2,3,4,5,6),skip_header=1) 
data2 = numpy.genfromtxt(file2,dtype='str',delimiter="\t") 

#get classes for later display in average statistics
classes = munger.getFirstRow(data2)
classes = classes[1:6]

#Clean up of labels
data1 = munger.deleteFirstCol(data1)
data2 = munger.deleteFirstRow(data2)
data2 = munger.deleteFirstCol(data2)

data1f = data1.astype(float)    #convert to floats
data2f = data2.astype(float)

diff = data2f-data1f    #take the difference of the two arrays
diff = abs(diff)

#get total avg. error
totalAvgError = numpy.sum(diff)/diff.size
print "Average difference over all classes: "+str(totalAvgError)+'%'

#get total elements >5% error
MoreFivePercentError = diff > .05
MoreFivePercent=numpy.sum(MoreFivePercentError)
print "Total number of elements with greater than 5'%' difference: "+str(MoreFivePercent) 
  
#get total elements >10% error
MoreTenPercentError = diff > .10
MoreTenPercent=numpy.sum(MoreTenPercentError)
print "Total number of elements with greater than 10'%' difference: "+str(MoreTenPercent) 

#get total elements >50% error
MoreFiftyPercentError = diff > .5
MoreFiftyPercent=numpy.sum(MoreFiftyPercentError)
print "Total number of elements with greater than 50'%' difference: "+str(MoreFiftyPercent) 

#get column avg. error
for n in xrange(1,6):
    col = munger.getNthCol(diff,n)
    colAvg = numpy.sum(col)/col.size
    colMax = col.max()
    colMin = col.min()
    print "\""+classes[n-1]+"\""
    print "\t"+"avg difference: "+str(colAvg)
    print "\t"+"max difference: "+str(colMax)
    print "\t"+"min difference: "+str(colMin)