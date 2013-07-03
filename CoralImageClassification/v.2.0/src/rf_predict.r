library('randomForest')
data <- read.delim('output/WLH2.output.txt')
data <- data[,1:(ncol(data)-1)]
data <- data[complete.cases(data),]
rf=randomForest(data[,3:ncol(data)], data[,2], importance=TRUE, ntrees=50000)
p <- predict(rf, data, 'prob')
write.table(p, file='WLH2.probabilities.txt', sep='\t')
