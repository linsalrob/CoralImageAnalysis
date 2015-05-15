import sys
sys.path.append('../Modules/')
import Contours
import cv2

im = cv2.imread('test.jpg')
g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

c = Contours.contours(g)

print "Threshold\t# contours\tNum lines\tNum lens\tMax\tMean\tMode\tMedian"
for i in range(5):
    thresh = 50*i
    c.withCanny(1, thresh)
    # print "\t".join(map(str, [thresh, c.numberOfContours(), c.numberOfClosedContours(),
    #                    c.numberOfOpenContours(), c.totalContourArea(), cv2.contourArea(c.largestContourByArea()),
    #                    c.totalPerimeterLength()]))

    print thresh, "\t",
    print c.numberOfContours(), "\t",
    print len(c.findLines()), "\t",
    print len(c.linelengths()), "\t",
    print c.maxLineLength(), "\t",
    print c.meanLineLength(), "\t",
    print c.modeLineLength(), "\t",
    print c.medianLineLength(), "\t"


