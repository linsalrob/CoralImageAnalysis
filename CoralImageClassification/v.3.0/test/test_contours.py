import sys
sys.path.append('../Modules/')
import Contours
import cv2

im = cv2.imread('test.jpg')
g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

c = Contours.contours(g)

print "Threshold\t# contours\tClosed\tOpen\tTotal area\tLargest\tPerimeter"
for i in range(5):
    thresh = 50*i
    c.withCanny(1, thresh)
    # print "\t".join(map(str, [thresh, c.numberOfContours(), c.numberOfClosedContours(),
    #                    c.numberOfOpenContours(), c.totalContourArea(), cv2.contourArea(c.largestContourByArea()),
    #                    c.totalPerimeterLength()]))

    print thresh, "\t",
    print c.numberOfContours(), "\t",
    print c.numberOfClosedContours(), "\t",
    print c.numberOfOpenContours(), "\t",
    print c.totalContourArea(), "\t",
    print cv2.contourArea(c.largestContourByArea()), "\t",
    print c.totalPerimeterLength()


