import numpy
import cv
import AnalyzeStatistics
import string
import time
import threading
import sys
import os

##cv.SaveImage(filename + number + "RED.jpg", imgoutred)

def normalize():
    for j in range(norm.height):
        for i in range(norm.width):
            sumrgb = norm[j,i][0] + norm[j,i][1] + norm[j,i][2]
            b = (norm[j,i][0]/sumrgb)*255
            g = (norm[j,i][1]/sumrgb)*255
            r = (norm[j,i][2]/sumrgb)*255
            norm[j,i] = [b,g,r]


#Column format:
#columnname, a.variablename
analyzeBase = AnalyzeStatistics.Analysis('base')
analyzeNorm = AnalyzeStatistics.Analysis('norm')

analyses = [analyzeBase,analyzeNorm]  

inputdir = "Images"
outfile = "outdata.txt"
classFile = "NKH_ATRIS+ADAPT.txt"
classInput = open(classFile, 'r')

classifiedNames = []
for line in classInput:
    tokens = line.split('\t')
    if tokens[10].strip() != '-':
        if os.path.isfile(inputdir + '/' + tokens[0].strip()):
            classifiedNames.append([os.path.join(inputdir, tokens[0].strip()), tokens[10].strip()])


##################################################


f = open(outfile, 'w')
first = True
f.write('imageName\tclassification\t')
for x in analyses:
    for col in x.getcolumnform():
        if(first == False):
            f.write("\t")
        f.write(x.name + "_" + col[1])
        first = False

f.write("\n")


for x in classifiedNames:
    filename = x[0]
    print 'Starting: ' + x[0]
    img = cv.LoadImage(filename)
    norm = cv.LoadImage(filename)
    tStart = time.clock()
    print 'Start normalizing...'
    for j in range(norm.height):
        for i in range(norm.width):
            sumrgb = norm[j,i][0] + norm[j,i][1] + norm[j,i][2]
            b = (norm[j,i][0]/sumrgb)*255
            g = (norm[j,i][1]/sumrgb)*255
            r = (norm[j,i][2]/sumrgb)*255
            norm[j,i] = [b,g,r]
    print 'Done normalizing.'
    print '      |---1234567890|'
    tStop = time.clock()
    #print 'norming: ' + str(tStop-tStart)
    sys.stdout.write('Raw:  ')
    analyzeBase.begin(img,0,1)
    sys.stdout.write('Norm: ')
    analyzeNorm.begin(norm,1,1)

    print 'Ending: ' + x[0]

    outline = x[0][7:]
    outline += '\t'
    outline += x[1]
    for x in analyses:
        for col in x.getcolumnform():
            outline += '\t'
            outline += str(x.getvar(col[1], col[2]))
    outline += '\n'
    f.write(outline)
f.close()


