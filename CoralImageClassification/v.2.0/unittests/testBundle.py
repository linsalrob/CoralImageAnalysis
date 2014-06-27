#TestBundle.py
#A basic bundle script, which runs unittests for classes in Modules.

import os
def printRunning(process):
    current = "Running "+process+ "..."
    print current
    
def run(process):
    printRunning(process)
    os.system("python "+process)

testList = [
    "test_analysis_unittest.py",
    "test_classification_unittest.py",
    "test_contours_unittest.py",
    "test_imageio_unittest.py",
    "test_normalization_unittest.py"]
for file in testList:
    run(file)

"""
print "Starting unit tests..."
printRunning("test_analysis_unittest.py")
os.system("python test_analysis_unittest.py")

printRunning("test_classification_unittest.py")
os.system("python test_classification_unittest.py")

printRunning("test_contours_unittest.py")
os.system("python test_contours_unittest.py")

printRunning("test_imageio_unittest.py")
os.system("python test_imageio_unittest.py")

printRunning("test_normalization_unittest.py")
os.system("python test_normalization_unittest.py")
"""
