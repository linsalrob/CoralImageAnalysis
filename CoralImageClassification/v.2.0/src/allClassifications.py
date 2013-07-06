

import sys
sys.path.append('../Modules/')
import Classification

classification={}
for d in range(1, len(sys.argv)):
    classificationFile = sys.argv[d]
    sys.stderr.write("Parsing " + classificationFile + "\n")
    p = Classification.Parsers(classificationFile)
    newclass=p.zawada()
    for i in newclass:
        if i in classification and classification[i] != '' and classification[i] != newclass[i]:
            sys.stderr.write("Overwriting " + classification[i] + " with " + newclass[i] + "\n")
            classification[i]=newclass[i]
        else:
            classification[i]=newclass[i]


for i in classification:
    print "\t".join([i, classification[i]])
