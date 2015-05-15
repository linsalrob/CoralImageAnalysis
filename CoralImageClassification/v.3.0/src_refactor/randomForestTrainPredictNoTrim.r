# this script uses a single data file for training and prediction

args <- commandArgs(trailingOnly = TRUE)
datafile = args[1]

print(paste("Data set of images :", datafile, sep=" "))



library('randomForest')
# is we always set the same seed we will always get the same result
set.seed(113) 
data <- read.delim(datafile)
data[,2]<-factor(data[,2])

print(paste("Number of rows and columns in the data file:", nrow(data), "x", ncol(data), sep=" "))

# remove any cases where we don't have classification data
training <- subset(data, data[,2]!='') #This used to be 'Unknown', but the values are deliniated at '' to indicate no classification
training[,2] <- factor(training[,2])
training <- training[complete.cases(training),]
print(paste("Number of rows and columns in the training set:", nrow(training), "x", ncol(training), sep=" "))

rf=randomForest(training[,3:ncol(training)], training[,2], importance=TRUE, ntrees=100001)
rf
rffile=paste("rf/", datafile, ".rf.bin", sep="")
save(rf, file=rffile)


outfile=paste("png/", datafile, "_imp.png", sep="")
png(outfile)
par(mfrow=c(2,1))
par(pty="s")
varImpPlot(rf, type=1, pch=19, col=1, cex=.5, main="")
varImpPlot(rf, type=2, pch=19, col=1, cex=.5, main="")
dev.off()

dataNoN <- na.omit(data)
p <- predict(rf, dataNoN, 'prob')
namedp <- data.frame(dataNoN[1], p)
outtext = paste("probabilities/", datafile, ".probabilities.txt", sep="")
write.table(namedp, file=outtext, sep='\t')
