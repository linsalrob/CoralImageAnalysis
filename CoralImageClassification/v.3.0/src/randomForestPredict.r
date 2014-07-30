# this script uses a single data file for training and prediction

args <- commandArgs(trailingOnly = TRUE)
datafile = args[1]

print(paste("Data set of images :", datafile, sep=" "))



library('randomForest')
# is we always set the same seed we will always get the same result
set.seed(113) 
data <- read.delim(datafile)
data[,2]<-factor(data[,2])

rffile=paste("rf/", datafile, ".rf.bin", sep="")
load(rffile)

p <- predict(rf, data, 'prob')
namedp <- data.frame(data[1], p)
outtext = paste(datafile, ".probabilities.txt", sep="")
write.table(namedp, file=outtext, sep='\t')
