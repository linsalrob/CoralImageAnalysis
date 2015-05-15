#Python rewrite of randomForestPredictNoTrim.r for Coral Reef Classification project
#Uses scikit python module


import sys
sys.path.append('../Modules/')
import munger
import argparse
import csv
import numpy
import time

import cPickle  
from sklearn.ensemble import RandomForestClassifier



infile = sys.argv[1]
print "Data set of images: "+infile+"."   
file = open(infile,"r")   #open file in readonly mode
data = numpy.genfromtxt(file,dtype='str',delimiter="\t") #strips data out of file, and creates ndarray of strings

badVarSpc=""   #!!!Note: original version looked for 'Unknown' as the token which indicated an undesirable row.
            #However, I looked at the ELH2.all.features.txt in 'previous_analysis' and it looks blanks indicate that 
            #a row is not classified.
badVarUnk="Unknown"
training = data[data[:,1] != badVarSpc] #check data for spaces
training = training[training[:,1] != badVarUnk] #check remaining values for 'unknown' values

training = munger.deleteFirstRow(training)  #removes first row (info about what columns are)

rf = RandomForestClassifier(n_estimators=501,max_features=8,oob_score=True,n_jobs=4,random_state=113) #was 10001 trees, but reduced for testing
#rf = RandomForestClassifier(n_estimators=10) #pure for test, no extra stuff, to decrease time taken in processing

inputs = training 
inputs = inputs[~(inputs=='nan').any(axis=1)]  #check for any columns with 'nan' data, if found, delete the row containg the column.
classifications=munger.getNthCol(inputs,2)
inputs = munger.deleteColSequence(inputs,1,2) #delete image names and classifications.
inputs = inputs.astype(float) 
classifications = numpy.ravel(classifications) #Flatten into a 1D array

beforeTime=time.clock() 
#forest=rf.fit(inputs,classifications)
forest=rf.fit(inputs,classifications)
afterTime=time.clock()
diffTime=afterTime-beforeTime
print "Time taken to fit forest: "+str(diffTime)

forestFileName="rf/"+infile+".rf.bin"

outForest = open(forestFileName,'wb')
cPickle.dump(forest,outForest)
#with open(forestFileName,'wb') as f:
    #cPickle.dump(forest,f)

#This is how you open the pickled randomForest
#with open(forestFileName,'rb') as f:
#    testForest = cPickle.load(f)


data = munger.deleteFirstRow(data) #clean off column descriptors
data = data[~(data=='nan').any(axis=1)] #check data for 'nan's and remove row if found
names = munger.getFirstCol(data) #get names for picture which row describes
data = munger.deleteColSequence(data,1,2) #delete names and classifications.

predict = forest.predict_proba(data)
classes = forest.classes_
classes = numpy.hstack(("Image File",classes))

predict=numpy.hstack((names,predict))
predict=numpy.vstack((classes,predict))

infile = infile[:-4]    #clean up infile name, remove .txt
outfileName = "probabilities/"+infile+".probabilities.txt"
print "Wrote "+outfileName
outfile = open(outfileName,"w")
numpy.savetxt(outfile,predict,fmt="%s",delimiter="\t",newline="\n")
outfile.close()


"""OUTLINE FOR PROGRAM"""
#args <- commandArgs(trailingOnly = TRUE)
#datafile = args[1]

#print(paste("Data set of images :", datafile, sep=" "))

#library('randomForest')
# is we always set the same seed we will always get the same result
#set.seed(113) 
#data <- read.delim(datafile)

"""SKIPPED"""
#data[,2]<-factor(data[,2])
#!!!NOTE: second column is classifications
""""""

#print(paste("Number of rows and columns in the data file:", nrow(data), "x", ncol(data), sep=" "))



# remove any cases where we don't have classification data
#training <- subset(data, data[,2]!='Unknown')

"""SKIPPED"""
#training[,2] <- factor(training[,2])
#training <- training[complete.cases(training),]
""""""

#print(paste("Number of rows and columns in the training set:", nrow(training), "x", ncol(training), sep=" "))


#rf=randomForest(training[,3:ncol(training)], training[,2], importance=TRUE, ntrees=100001)
#rf

#rffile=paste("rf/", datafile, ".rf.bin", sep="")
#save(rf, file=rffile)

"""SKIPPED"""
#outfile=paste("png/", datafile, "_imp.png", sep="")
#png(outfile)
#par(mfrow=c(2,1))
#par(pty="s")
#varImpPlot(rf, type=1, pch=19, col=1, cex=.5, main="")
#varImpPlot(rf, type=2, pch=19, col=1, cex=.5, main="")
#dev.off()
""""""

"""WORKING HERE"""

"""SKIPPED"""
#dataNoN <- na.omit(data)
#this seems to remove any data 'rows which have 'NA' values , but I don't think there are any?
""""""

#p <- predict(rf, dataNoN, 'prob')
#namedp <- data.frame(dataNoN[1], p)
#outtext = paste("probabilities/", datafile, ".probabilities.txt", sep="")
#write.table(namedp, file=outtext, sep='\t')
