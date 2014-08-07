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
"python ../src/analyzeDZImages.py -d /data/Zawada/ATRIS_images/WLH1 -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsA.txt -o WLH1.output.tsv",
"python ../src/analyzeDZImages.py -d /data/Zawada/ATRIS_images/WLH1 -a -o WLH1.allimages.tsv",
"python ../src/analyzeDZImages.py -d /data/Zawada/ATRIS_images/WLH1 -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsA.txt -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsB.txt -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsB_1_3.txt -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsC.txt -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsD.txt -o WLH1.all.tsv -a",
"python ../src/featureDetection.py -d /data/Zawada/ATRIS_images/ELH2/ -o ELH2.features.tsv",
"perl ../src/join.pl ELH2.features.tsv ELH2.all.txt > ELH2.all.features.tsv",
"python ../src_refactor/randomForest_Refactor.py WLH1.output.tsv",
"Rscript ../src/randomForestTrainPredict.r LHM5.all.tsv",
"python ../src_refactor/randomForestTrainPredictNoTrim_Refactor.py ELH2.all.features.tsv",
"python ../src/plot_predictions.py -f WLH1.output.probabilities.tsv -o WLH1.png"] #reflects better naming conventions.
script1 = ["python","../src/analyzeDZImages.py","-d /data/Zawada/ATRIS_images/WLH1","-f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsA.txt","-o WLH1.output.tsv"]
script2 = ["python","../src/analyzeDZImages.py","-d /data/Zawada/ATRIS_images/WLH1","-a -o WLH1.allimages.tsv"]
script3 = []


scriptsNew = [script1,script2]
for script in scriptsNew:
        print script[0]
        subprocess.call(script)
        
 
"""
for script in scripts:
    try:
        errorString = "FAILED: "+script
        print "Starting "+script
        print ""
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
"""      
outfile.close()