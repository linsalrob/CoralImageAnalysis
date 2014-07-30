# this script uses a single data file for training and prediction

args <- commandArgs(trailingOnly = TRUE)
datafile = args[1]

print(paste("Data set of images :", datafile, sep=" "))



library('randomForest')
# is we always set the same seed we will always get the same result
set.seed(113) 
data <- read.delim(datafile)
# trim off the last column which is all NA
data <- data[,1:(ncol(data)-1)]
data[,2] <- as.character(data[,2])
for (k in (1:nrow(data))) {
	if (is.na(data[k,2]) || data[k,2] == '') {
		data[k,2] <- 'Unknown'
	}
}
data[,2]<-factor(data[,2])

# remove any cases where we don't have classification data
training <- subset(data, data[,2]!='Unknown')
training[,2] <- factor(training[,2])
#training <- training[complete.cases(training),]

rf=randomForest(training[,3:ncol(training)], training[,2], importance=TRUE, ntrees=100001)
rf
outfile=paste("png/", datafile, "_imp.png", sep="")
png(outfile)
par(mfrow=c(2,1))
par(pty="s")
varImpPlot(rf, type=1, pch=19, col=1, cex=.5, main="")
varImpPlot(rf, type=2, pch=19, col=1, cex=.5, main="")
dev.off()



p <- predict(rf, data, 'prob')
namedp <- data.frame(data[1], p)
outtext = paste(datafile, ".probabilities.txt", sep="")
write.table(namedp, file=outtext, sep='\t')
