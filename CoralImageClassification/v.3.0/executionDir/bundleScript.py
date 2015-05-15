#Bundle python script for CS Lab
import os
import subprocess
import time as t
#os.system('echo "test!"')
#subprocess.call(["echo","test!"])
errorString = "Entering Loop."
programStart = t.time()
start = 0
end = 0
ret = 0 #returned value from os calls

outfileName = "bundle-script-log"+t.strftime("_%a-%d-%b-%H:%M:%S")+".txt"
outfile = open(outfileName,"w")

scripts = [
"python ../src/analyzeDZImages.py -d /data/Zawada/ATRIS_images/WLH1 -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsA.txt -o WLH1.output.txt",
"python ../src/analyzeDZImages.py -d /data/Zawada/ATRIS_images/WLH1 -a -o WLH1.allimages.txt",
"python ../src/analyzeDZImages.py -d /data/Zawada/ATRIS_images/WLH1 -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsA.txt -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsB.txt -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsB_1_3.txt -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsC.txt -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsD.txt -o WLH1.all.txt -a",
"python ../src/featureDetection.py -d /data/Zawada/ATRIS_images/ELH2/ -o ELH2.features.txt",
"perl ../src/join.pl ELH2.features.txt ELH2.all.txt > ELH2.all.features.txt",
"Rscript ../src/randomForest.r WLH1.output.txt",
"Rscript ../src/randomForestTrainPredict.r LHM5.all.txt",
"Rscript ../src/randomForestTrainPredictNoTrim.r ELH2.all.features.txt",
"python ../src/plot_predictions.py -f WLH1.output.txt.probabilities.txt -o WLH1.png"]

for script in scripts:
    try:
        errorString = "FAILED: "+script
        print "Starting "+script
        start = t.time()
        ret = os.system(script)
        if(ret != 0):
            raise RuntimeError(errorString)
        end = t.time()
        diff = end-start
        diff = diff/60 #conversion to minutes
        msg = str(diff)+" minutes   : "+script
        outfile.write(msg)
        outfile.write("\n")
        print msg
        
    except RuntimeError:
        print "Error "+ errorString
        end = t.time()
        diff = end-start
        diff = diff/60
        msg = str(diff)+" minutes   : "
        outfile.write(msg+" "+errorString)
        outfile.write("\n")
        
outfile.close()

"""try:
    errorString = "in analyzeDZImages.py single image."
    print "Starting analyzeDZImages.py on a single image set."
    start = t.time()
    ret = os.system("python ../src/analyzeDZImages.py -d /data/Zawada/ATRIS_images/WLH1 -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsA.txt -o WLH1.output.txt")
    if(ret != 0):
        raise RuntimeError(errorString)
    end = t.time()
    diff = end-start
    
    msg = "analyzeDZImages.py took "+str(diff)+" seconds."
    outfile.write(msg)
    print msg
    
    #artificial delay
    #current = t.time()
    #end = start+10
    #while(current<end):
    #    current = t.time()
    
    errorString = "in analyzeDZImages.py group set."
    print "Starting analyzeDZImages.py on a 'group' of image sets."
    start = t.time()
    ret = os.system("python ../src/analyzeDZImages.py -d /data/Zawada/ATRIS_images/WLH1 -a -o WLH1.allimages.txt")
    if(ret != 0):
        raise RuntimeError(errorString)
    end = t.time()
    diff = end-start
    
    msg = "analyzeDZImages.py took "+str(diff)+" seconds."
    outfile.write(msg)
    print msg
    
    errorString = "in analyzeDZImages.py on all image sets"
    print "Starting analyzeDZImages.py on all image sets."
    start = t.time()
    ret = os.system("python ../src/analyzeDZImages.py -d /data/Zawada/ATRIS_images/WLH1 -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsA.txt -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsB.txt -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsB_1_3.txt -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsC.txt -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsD.txt -o WLH1.all.txt -a")
    if(ret != 0):
        raise RuntimeError(errorString)
    end = t.time()
    diff = end-start
    print "analyzeDZImages.py took "+str(diff)+" seconds."
    
    errorString = "in featureDetection.py"
    print "Starting featureDetection.py."
    start = t.time()
    ret = os.system('python ../src/featureDetection.py -d /data/Zawada/ATRIS_images/ELH2/ -o ELH2.features.txt')
    if(ret != 0):
        raise RuntimeError(errorString)
    end = t.time()
    diff = end-start
    print "featureDetection.py took "+str(diff)+" seconds."

    errorString = "in join.pl."
    print "Starting join.pl."
    start = t.time()
    ret = os.system('perl ../src/join.pl ELH2.features.txt ELH2.all.txt > ELH2.all.features.txt')
    if(ret != 0):
        raise RuntimeError(errorString)
    end = t.time()
    diff = end-start
    print "join.pl took "+str(diff)+" seconds."
    
    errorString = "in randomForestTrainPredict.r"
    print "Starting randomForestTrainPredict.r."
    start = t.time()
    ret = os.system('Rscript ../src/randomForestTrainPredict.r LHM5.all.txt')
    if(ret != 0):
        raise RuntimeError(errorString)
    end = t.time()
    diff = end-start
    print "randomForestTrainPredict.r took "+str(diff)+" seconds."
    
    errorString = "in randomForestTrainPredictNoTrim.r"
    print "Starting randomForestTrainPredictNoTrim.r."
    start = t.time()
    ret = os.system('Rscript  ../src/randomForestTrainPredictNoTrim.r ELH2.all.features.txt')
    if(ret != 0):
        raise RuntimeError(errorString)
    end = t.time()
    diff = end-start
    print "randomForestTrainPredictNoTrim.r took "+str(diff)+" seconds."
    
    
    #os.system()
except RuntimeError:
    print "Error "+ errorString
"""
