
# coding: utf-8
import matplotlib
matplotlib.use('agg')
from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
import numpy
import sys
import argparse

parser = argparse.ArgumentParser(description='Plot the predictions made by the Random Forest')
parser.add_argument('-f', '--file', help='tab separated predictions from the Random Forest', required=True)
parser.add_argument('-o', '--out', help='output file name to draw the picture to', required=True)
parser.add_argument('-w', '--window', help='Window size to average the numbers over (try 1/100 * # images). If not provided the numbers are not averaged.')
args = parser.parse_args()


def movingaverage(interval, window_size):
    window= numpy.ones(int(window_size))/float(window_size)
    return numpy.convolve(interval, window, 'same')



fin = open(args.file, 'r')
header = None
data=[]
xlabels=[]
for line in fin:
    line = line.rstrip()
    line = line.replace('"', '')
    d = line.split('\t')
    if header == None:
        header=d[1:]
        continue
    xlabels.append(d[1])
    data.append(numpy.array(d[2:]).astype(float))

dtc=None
if args.window:
    dt=numpy.transpose(data)
    for i in range(dt.shape[0]):
        dt[i]=movingaverage(dt[i], args.window)
        
    dtc=numpy.transpose(dt)
else:
    dtc=data

fontP = FontProperties()
fontP.set_size('small')
fig = plt.figure()
ax = plt.subplot(111)
ax.plot(dtc)
#ax.set_xticklabels(xlabels, rotation=45, fontproperties=fontP)
#ax.set_xlabel('Image number in the series')
ax.set_ylabel('Image classification')
box = ax.get_position()
#ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height * 0.9])
#ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height])
ax.set_position([box.x0, box.y0 + box.height * 0.1, box.width, box.height *0.85])

ax.legend((header), loc='upper center', bbox_to_anchor=(0.5, -0.10), ncol=4, prop=fontP)
fig.savefig(args.out)

# plt.plot(dtc)
# plt.legend((header))
# plt.ylabel('Probability')
# plt.xlabel('Image number')
# plt.savefig(args.out)

