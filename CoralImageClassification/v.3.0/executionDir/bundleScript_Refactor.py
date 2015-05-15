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

outfileName = "bundle-script-log"+t.strftime(":%a-%d-%b-%H:%M:%S")+".txt"
outfile = open(outfileName,"w")
outfile.close()

scripts = [
"python ../src_refactor/analyzeDZImages_Refactor_Map.py -d /data/Zawada/ATRIS_images/WLH1 -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsA.txt -o WLH1.output.tsv",
"python ../src_refactor/analyzeDZImages_Refactor_Map.py -d /data/Zawada/ATRIS_images/WLH1 -a -o WLH1.allimages.tsv",
"python ../src_refactor/analyzeDZImages_Refactor_Map.py -d /data/Zawada/ATRIS_images/WLH1 -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsA.txt -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsB.txt -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsB_1_3.txt -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsC.txt -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsD.txt -o WLH1.all.tsv -a",
"python ../src_refactor/featureDetectionJoin.py",
#"python ../src_refactor/featureDetection_Refactor_Map.py -d /data/Zawada/ATRIS_images/ELH2/ -o ELH2.features.tsv",
#"perl ../src/join.pl ELH2.features.tsv ELH2.all.txt > ELH2.all.features.tsv",
"python ../src_refactor/randomForest_Refactor.py WLH1.output.tsv",
"Rscript ../src/randomForestTrainPredict.r LHM5.all.txt", #I'm not sure if this is needed.
#"python ../src_refactor/randomForestTrainPredict_Refactor.py ELH2.all.features.tsv",
#This is not implemented yet ^
"python ../src_refactor/randomForestTrainPredictNoTrim_Refactor.py ELH2.all.features.tsv",
"python ../src/plot_predictions.py -f WLH1.output.probabilities.tsv -o WLH1.png",
"perl ../src/concatenate.pl *all.features.tsv > all.all.tsv",
"mv *all.features.tsv all_features/",
"for i in ELH1 ELH2 LHM5 WLH1 WLH2; do perl ../src/clean_output.pl all_features/$i.all.features.tsv $i.data.tsv; done",
"for i in ELH1  LHM5  WLH1  WLH2; do python ../src_refactor/randomForestTrainPredictNoTrim_Refactor.py $i.data.tsv > rf_output/$i.rf.out.tsv; done",
"perl ../src/concatenate.pl *.data.tsv > all.data.tsv",
"python ../src_refactor/randomForestTrainPredictNoTrim_Refactor.py all.data.tsv > rf_output/all.rf.out"
]

for script in scripts:
    try:
        errorString = "FAILED: "+script
        print ""
        print " * * * * * * * * * * * "
        print "Starting "+script
        print ""
        outfile = open(outfileName,"a")
        outfile.write("\n")
        outfile.write(" * * * * * * * * * * * ")
        outfile.write("\n")
        outfile.write("Starting "+script)
        outfile.write("\n")
        outfile.close()
        start = t.time()
        ret = os.system(script)
        if(ret != 0):
            raise RuntimeError(errorString)
        end = t.time()
        diff = end-start
        diff = diff/60 #conversion to minutes
        msg = "Took "+str(diff)+" minutes. "
        outfile = open(outfileName,"a")
        outfile.write(msg)
        outfile.write("\n")
        outfile.close()
        
    except RuntimeError:
        print "Error "+ errorString
        end = t.time()
        diff = end-start
        diff = diff/60
        msg = "Took "+str(diff)+" minutes."
        outfile = open(outfileName,"a")
        outfile.write(errorString)
        outfile.write("\n")
        outfile.write(msg)
        outfile.write("\n")
        outfile.close()
