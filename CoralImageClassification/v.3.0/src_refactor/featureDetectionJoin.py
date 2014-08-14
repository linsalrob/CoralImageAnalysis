#featureDetectionJoin.py
import os
fileNames =  ["ELH1", "ELH2", "LHM5", "WLH1", "WLH2"]
for name in fileNames:
    script = "python ../src_refactor/featureDetection_Refactor_Map.py -d /data/Zawada/ATRIS_images/"+name+"/ -o "+name+".features.tsv"
    ret = os.system(script)

for name in fileNames:
    script = "perl ../src/join.pl "+name+".features.txt "+name+".all.txt > "+name+".all.features.txt"
    ret = os.system(script)

#for i in ELH1 ELH2 LHM5 WLH1 WLH2; do python ../src_refactor/featureDetection_Refactor_Map.py -d /data/Zawada/ATRIS_images/$i/ -o $i.features.tsv; done


#perl ../src/join.pl ELH2.features.txt ELH2.all.txt > ELH2.all.features.txt

