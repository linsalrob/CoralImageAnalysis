## Read a randomForest library and then cross validate against all other data sets

library('randomForest')
# is we always set the same seed we will always get the same result
set.seed(113) 

for (name in c("ELH1.data.txt", "ELH2.data.txt", "LHM5.data.txt", "NKH.data.txt", "WLH1.data.txt", "WLH2.data.txt", "all.txt")) {
	rffile = paste("rf/", name, ".rf.bin", sep="")
	load(rffile)
	for (oname in c("ELH1.data.txt", "ELH2.data.txt", "LHM5.data.txt", "NKH.data.txt", "WLH1.data.txt", "WLH2.data.txt", "all.txt")) {
		datafile = oname
		print(paste("Comparing ", name, ".rf.bin and ", oname, sep=""))
		data <- read.delim(datafile)
		data <- na.omit(data)
		p <- predict(rf, data, 'prob')
		namedp <- data.frame(data[1], p)
		outtext = paste(oname, "_data.", name, "_rf.probabilities.txt", sep="")
		write.table(namedp, file=outtext, sep='\t')
	}
}
