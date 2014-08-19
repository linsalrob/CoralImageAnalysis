#clean.py
#Clean script for Coral Image Analysis executionDir
#Used to restore executionDir to original status.
import os
scripts = [
"rm bundle-script-log*",
"rm DZImages_Map_log*",
"rm *.tsv",
"rm all_features/*",
"rm png/*",
"rm probabilities/*",
"rm rf/*",
"rm rf_output/*"]

for script in scripts:
    try:
        
        errorString = "FAILED: "+script
        ret = os.system(script)
        if(ret != 0):
            raise RuntimeError(errorString)
        print script
    except RuntimeError:
        print errorString
        