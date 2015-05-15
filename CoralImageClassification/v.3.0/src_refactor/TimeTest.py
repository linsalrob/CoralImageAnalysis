#function for comparing old and refactored versions of code.

import os
import subprocess
import time as t
import shlex

outfileName = "test_result.txt"
"""
script1 = "python ../src/analyzeDZImages.py -d /data/Zawada/ATRIS_images/WLH1 -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsA.txt  -o WLH1.output.tsv"
script2 = "python ../src_refactor/analyzeDZImages_Refactor.py -d /data/Zawada/ATRIS_images/WLH1 -f /data/Zawada/ATRIS_images/PROCESSED/WLH1/WLH1_classificationsA.txt  -o WLH1.output_refactor.tsv"
"""

script1="python ../src/analyzeDZImages.py -d /data/Zawada/ATRIS_images/NKH2 -f /data/Zawada/ATRIS_images/PROCESSED/NKH2/NKH2_classifications.txt  -o NKH2.output.tsv"
script2="python ../src_refactor/analyzeDZImages_Refactor.py -d /data/Zawada/ATRIS_images/NKH2 -f /data/Zawada/ATRIS_images/PROCESSED/NKH2/NKH2_classifications.txt  -o NKH2.output_refactor.tsv"


start = t.time()
p = subprocess.Popen(shlex.split(script1))
p.wait()
end = t.time()
diff1 = end-start

start = t.time()
p = subprocess.Popen(shlex.split(script2))
p.wait()
end = t.time()
diff2 = end-start

totalDiff = diff1 - diff2
msg1 = "Time for original analyzeDZImages.py: "+str(diff1)
msg2 = "Time for refactored analyzeDZImages_Refactor.py: "+str(diff2)
msg3 = "Total Time difference is: "+str(totalDiff)

outfile = open(outfileName,"w")
outfile.write(msg1)
outfile.write("\n")
outfile.write(msg2)
outfile.write("\n")
outfile.write(msg3)
outfile.write("\n")
outfile.close()
