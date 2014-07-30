args <- commandArgs(trailingOnly = TRUE)
classified = args[1]
allimages = args[2]

print(paste("Classified images:", classified, sep=" "))
print(paste("All images:", allimages, sep=" "))



library('randomForest')
data <- read.delim(classified)
# trim off the last column which is all NA
data <- data[,1:(ncol(data)-1)]
data <- data[complete.cases(data),]
# remove any cases where we don't have classification data
data <- subset(data, data[,2]!='')
data <- subset(data, data[,2]!=0)
data[,2]<-factor(data[,2])

rf=randomForest(data[,3:ncol(data)], data[,2], importance=TRUE, ntrees=100001)
rf
outfile=paste("png/", classified, "_imp.png", sep="")
png(outfile)
par(mfrow=c(2,1))
par(pty="s")
varImpPlot(rf, type=1, pch=19, col=1, cex=.5, main="")
varImpPlot(rf, type=2, pch=19, col=1, cex=.5, main="")
dev.off()


unknowns <- read.delim(allimages)
unknowns <- unknowns[,1:(ncol(unknowns)-1)]

for (k in (1:nrow(unknowns))) {
	if (is.na(unknowns[k,2])) {
		unknowns[k,2]='unknown'
	}
}


p <- predict(rf, unknowns, 'prob')
namedp <- data.frame(unknowns[1], p)
outtext = paste(allimages, ".probabilities.txt", sep="")
write.table(namedp, file=outtext, sep='\t')
