## Read a randomForest library and then cross validate against all other data sets

library('randomForest')
# is we always set the same seed we will always get the same result
set.seed(113) 


#for (name in c("ELH1.data.txt",  "ELH2.data.txt",  "LHM5.data.txt",  "WLH1.data.txt",  "WLH2.data.txt")) {
#for (name in c("ELH1",  "ELH2",  "LHM5",  "WLH1",  "WLH2", "all")) {
#name="all"
#for (name in c("ELH1",  "ELH2",  "LHM5",  "WLH1",  "WLH2", "all", "all_not_ELH1", "all_not_ELH2", "all_not_LHM5", "all_not_WLH1", "all_not_WLH2")) {
for (name in c("EKC.data.txt", "ELH1.data.txt", "ELH2.data.txt", "LHM5.data.txt", "NKH.data.txt", "WLH1.data.txt", "WLH2.data.txt", "all.txt", "all_not_EKC.txt", "all_not_ELH2.txt", "all_not_NKH.txt", "all_not_WLH2.txt", "all_not_ELH1.txt", "all_not_LHM5.txt", "all_not_WLH1.txt")) {
	rffile = paste("rf/", name, ".rf.bin", sep="")
	load(rffile)
	#for (oname in c("ELH1",  "ELH2",  "LHM5",  "WLH1",  "WLH2", "all", "all_not_ELH1", "all_not_ELH2", "all_not_LHM5", "all_not_WLH1", "all_not_WLH2")) {
	for (oname in c("EKC.data.txt", "ELH1.data.txt", "ELH2.data.txt", "LHM5.data.txt", "NKH.data.txt", "WLH1.data.txt", "WLH2.data.txt", "all.txt", "all_not_EKC.txt", "all_not_ELH2.txt", "all_not_NKH.txt", "all_not_WLH2.txt", "all_not_ELH1.txt", "all_not_LHM5.txt", "all_not_WLH1.txt")) {
		#datafile = paste(oname, ".data.txt", sep="")
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
