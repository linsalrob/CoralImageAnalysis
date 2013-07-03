args <- commandArgs(trailingOnly = TRUE)
infile = args[1]
print(paste("Parsing", infile, sep=" "))

library('randomForest')
data <- read.delim(infile)
# trim off the last column which is all NA
data <- data[,1:(ncol(data)-1)]
data <- data[complete.cases(data),]
# remove any cases where we don't have classification data
data <- subset(data, data[,2]!=0)
data[,2]<-factor(data[,2])

rf=randomForest(data[,3:ncol(data)], data[,2], importance=TRUE, ntrees=100001)
rf
outfile=paste("png/", infile, "_imp.png", sep="")
png(outfile)
par(mfrow=c(2,1))
par(pty="s")
varImpPlot(rf, type=1, pch=19, col=1, cex=.5, main="")
varImpPlot(rf, type=2, pch=19, col=1, cex=.5, main="")
dev.off()
p <- predict(rf, data, 'prob')
outtext = paste(infile, ".probabilities.txt", sep="")
write.table(p, file=outtext, sep='\t')
