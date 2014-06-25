#TestBundle.py
#A basic bundle script, which runs unittests for classes in Modules.

import os

print "Starting unit tests..."
os.system("python test_analysis_unittest.py")
os.system("python test_classification_unittest.py")
os.system("python test_contours_unittest.py")
os.system("python test_imageio_unittest.py")
os.system("python test_normalization_unittest.py")
