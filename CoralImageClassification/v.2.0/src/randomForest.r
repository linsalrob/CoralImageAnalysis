args <- commandArgs(trailingOnly = TRUE)
infile = args[1]
print(paste("Parsing", infile, sep=" "))

library('randomForest')
data <- read.delim(infile)
data <- data[complete.cases(data),]
rf=randomForest(data[,3:(ncol(data)-1)], data[,2], importance=TRUE, ntrees=50000)
outfile=paste("png/", infile, "_imp.png", sep="")
png(outfile)
par(mfrow=c(2,1))
par(pty="s")
varImpPlot(rf, type=1, pch=19, col=1, cex=.5, main="")
varImpPlot(rf, type=2, pch=19, col=1, cex=.5, main="")
dev.off()
rf
