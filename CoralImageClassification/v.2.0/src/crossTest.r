
## Read a randomForest library and then cross validate against all other data sets

args <- commandArgs(trailingOnly = TRUE)
directory = args[1]

## Read a randomForest library and then cross validate against all other data sets

library('randomForest')
# is we always set the same seed we will always get the same result
set.seed(113) 

rflist = list.files(directory)
datalist <- unique(sub("[\\d\\.]*.rf.bin", "", rflist, perl=TRUE))

for (name in as.vector(rflist)) {
	rffile = paste(directory, "/", name, sep="")
	load(rffile)
	for (datafile in as.vector(datalist)) {
		print(paste("Comparing ", name, " and ", datafile, sep=""))
		data <- read.delim(datafile)
		data <- na.omit(data)
		p <- predict(rf, data, 'prob')
		namedp <- data.frame(data[1], p)
		outtext = paste(datafile, "_data.", name, "_rf.probabilities.txt", sep="")
		write.table(namedp, file=outtext, sep='\t')
	}
}
