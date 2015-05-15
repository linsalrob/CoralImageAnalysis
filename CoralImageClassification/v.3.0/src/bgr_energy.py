
import sys
sys.path.append('../Modules/')
import ImageIO
from Analysis import *

'''
A simple test whether the bgr_energy calculation works
'''

im = sys.argv[1]

img = ImageIO.cv2read(im)
fft=FFT()
for i in range(3):
    print "The energy for the ", i, " channel is ", fft.energy(img[:,:,i])

