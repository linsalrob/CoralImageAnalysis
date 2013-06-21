
''' A test suite written to test the image analysis code. 

All of these tests should pass'''

import sys
import ImageIO
from Analysis import *
import os

imageFile = 'test.jpg'
if not os.path.exists(imageFile):
    sys.stderr.write("The test image file " + imageFile + " does not exist! Can't complete tests");
    sys.exit(-1)

image = ImageIO.cv2read(imageFile)
grayscale = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

# test the statistics module

print "The following tests are performed on the grayscale image:"
print "\nTesting the stats class"
s=Stats()
print "Testing minimum: ", s.min(grayscale)
print "Testing maximum: ", s.max(grayscale)
print "Testing mean: ", s.mean(grayscale)
print "Testing median: ", s.median(grayscale)

print "\nTesting the fft class"
f=FFT()
print "Testing FFT: "
ff=f.fft(grayscale)
print "Testing the energy: ", f.energy(grayscale)

print "\nTesting the feature detection"
sf = Features()
#print "Testing the laplacian: ", sf.get_laplacian(grayscale)

print "\nTesting the edge detection"
e = Edges()
print "Testing Canny"
c = e.Canny(grayscale)
print "Testing the sum: ", e.sumCanny(grayscale)



