#Python rewrite of randomForest.r for Coral Reef Classification project
#Uses scikit python module
import argparse
import sys
import csv
import numpy
import time
import munger
#from numpy import ndarray
from sklearn.ensemble import RandomForestClassifier

infile = sys.argv[1]
print "Parsing "+infile+"."   

file = open(infile,"r")   #open file in readonly mode
data = numpy.genfromtxt(file,dtype='str',delimiter="\t") #strips data out of file, and creates ndarray of strings



data = munger.deleteLastCol(data) #this is equal to data <- data[,1:(ncol(data)-1)]
#COME BACK AND DO THIS HERE
#data <- data[complete.cases(data),]
    #this looks for NA's
    #the syntax indicates that it is searching all rows
    #http://www.statmethods.net/input/missingdata.html
    #has a great example of code, very similar to this
    #seems to indicate that the code here removes any rows with NA's

badVar=""
data = data[data[:,1] != badVar] #Note ndarray is zero base, thus '1' is the second value

#rf = RandomForestClassifier(n_estimators=10,max_features=None,oob_score=True) #was 10001 trees, but reduced for testing

rf = RandomForestClassifier(n_estimators=5) #pure test, no extra stuff, to decrease time taken in processing
data = munger.deleteFirstRow(data) #removes first row
#classifications_old=data[0:,1] #This is an array of the second column of the file, a text representation of the classification.
classifications=munger.getNthCol(data,2)
classifications=numpy.ravel(classifications) #reformat data into a 1-D array, instead of a slice.


"""TESTING AREA"""

#stuff here is for processing secondary sets of data for testing
#testSet = sys.argv[2]   #allow a second argument to be supplied for testing RandomForest
#print "Test Set: "+testSet+"." 
#testfile = open(testSet,"r")   #open file in readonly mode
#testdata = numpy.genfromtxt(testfile,dtype='str',delimiter="\t") #strips data out of file, and creates ndarray of strings

#testdata = testdata[:,:-1]  #this is equal to data <- data[,1:(ncol(data)-1)]
#print "before: "+str(len(testdata))
#testdata = testdata[testdata[:,1] != badVar] 
#print "after: "+str(len(testdata))
#actualTest = testdata[:,1]   #grab second column, the classifications
#actualTest = actualTest[1:]   #remove first row, the label

#testdata=testdata[1:]
#testsizex=len(testdata[0])
#testsizey=len(testdata)

#testx=testdata[:testsizey,2: ]
#print str(testsizex)+" by "+str(testsizey)
#print "Done with test parsing."

"""END TEST AREA"""

sizex=len(data[0])
sizey=len(data)
#inputs=data[:sizey,2: ] #removes first and second column from all rows
inputs=munger.deleteColSequence(data,1,2)
beforeTime=time.clock() 

forest=rf.fit(inputs,classifications)
#predicted=forest.predict(inputs)
#applied=forest.apply(testx)
#acc=forest.score(testx,actualTest)
#acc=forest.score(inputs,classifications)

afterTime=time.clock()
diffTime=afterTime-beforeTime



#Skipped drawing these png images.
#I think they are for human reading only; even then, not really.

predict=forest.predict_proba(inputs)
#predict=predict.reshape(6,)
classes = forest.classes_

#predict=predict.transpose()
print predict.shape
print classes.shape

#print str(len(predict[0]))
#print str(len(predict))
#predict=predict.transpose()
#predict = predict.reshape(3759,6)
#predict=numpy.concatenate((predict,classes))
predict=numpy.vstack((classes,predict)) #add classes on top of 
print predict

outfileName=infile+".probabilities_refactor.txt"
outfile = open(outfileName,"w")
#classes.tofile(outfile,sep="\t")
#outfile.write("\n")
#predict.tofile(outfile,sep="\t")
numpy.savetxt(outfile,predict,fmt="%s",delimiter="\t",newline="\n")
outfile.close()


"""OUTLINE FOR PROGRAM"""

#args <- commandArgs(trailingOnly = TRUE)
#infile = args[1]
    #get trailing args

#print(paste("Parsing", infile, sep=" "))
    #print brief statement about which file is being parsed

#library('randomForest')
#data <- read.delim(infile)
    #read in file as a variable

# trim off the last column which is all NA
#data <- data[,1:(ncol(data)-1)]


#data <- data[complete.cases(data),]
    #this looks for NA's
    #the syntax indicates that it is searching all rows
    #http://www.statmethods.net/input/missingdata.html
    #has a great example of code, very similar to this
    #seems to indicate that the code here removes any rows with NA's

# remove any cases where we don't have classification data
#data <- subset(data, data[,2]!=0)
 
#data[,2]<-factor(data[,2])
    #Convert to factors, relevant in R, I'm not sure it's as relevant here

#rf=randomForest(data[,3:ncol(data)], data[,2], importance=TRUE, ntrees=100001)
#rf
    #start a random forest where x is a vector of the 3rd column of data, y is 2nd column of data, importance=TRUE,             ntrees=100001
    
#outfile=paste("png/", infile, "_imp.png", sep="")
#png(outfile)
    #make an outfile
    #make that outfile a png

 

#par(mfrow=c(2,1))
#par(pty="s")
    #http://www.statmethods.net/advgraphs/layout.html  info about par() and mfrow()
    #what par() is for combining multiple plots into one graph
    #mfrow is for creating a matrix of size (nrows, ncols)

#varImpPlot(rf, type=1, pch=19, col=1, cex=.5, main="")
#varImpPlot(rf, type=2, pch=19, col=1, cex=.5, main="")
    #http://cran.r-project.org/web/packages/randomForest/randomForest.pdf pg 27 has info about varImpPlot
    #is a 'Dotchart of variable importance as measured by a Random Forest'
    

#dev.off()
    #http://www.inside-r.org/r-doc/grDevices/dev.off
    #appears to be for graphics handling in R, a way to close a stream?

"""WORKING HERE""" 

#p <- predict(rf, data, 'prob')
    #http://cran.r-project.org/web/packages/randomForest/randomForest.pdf pg 15 has info about predict()
    #seems to be a probability prediction using the random forest on the imported 'data'.

#outtext = paste(infile, ".probabilities.txt", sep="")
    #create variable name out of infile and a new suffix
    
#write.table(p, file=outtext, sep='\t')
    #http://stat.ethz.ch/R-manual/R-devel/library/utils/html/write.table.html info about write.table
    #writes probability table to outfile seperated by a '\t'