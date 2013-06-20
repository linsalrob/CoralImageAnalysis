import sys


from ImageIO import cv2grayscale
from FFT import energy

im = sys.argv[1]

print "The energy is ", energy(cv2grayscale(im))
