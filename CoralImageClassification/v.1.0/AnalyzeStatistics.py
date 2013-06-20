import numpy
import cv
import time
import sys

class Analysis:
    def __init__(self, name):
        self.name = name
        self.aColors = True
        self.aSumLaplace = True
        self.aSumCanny = True
        self.aSumBinLaplace = True
        self.aSumFourier = False
        self.aSumBinFourier = False
        self.aSumLonersFourier = False
        self.aSumBinLonersFourier = False

    def begin(self, img, norm, subdepth):
        sys.stdout.write('|-')
        self.norm = norm
        self.img = img
        #Get each channel's image
        sys.stdout.write('-')
        igray = cv.CreateImage((self.img.width, self.img.height), self.img.depth, 1)
        cv.CvtColor(self.img, igray, cv.CV_BGR2GRAY)
        sys.stdout.write('-')
        self.blueChannel = cv.CreateImage((img.width, img.height), self.img.depth, 1)
        self.greenChannel = cv.CreateImage((img.width, img.height), self.img.depth, 1)
        self.redChannel = cv.CreateImage((img.width, img.height), self.img.depth, 1)
        self.fgrayChannel = cv.CreateImage((img.width, img.height), cv.IPL_DEPTH_32F, 1)
        self.fblueChannel = cv.CreateImage((img.width, img.height), cv.IPL_DEPTH_32F, 1)
        self.fgreenChannel = cv.CreateImage((img.width, img.height), cv.IPL_DEPTH_32F, 1)
        self.fredChannel = cv.CreateImage((img.width, img.height), cv.IPL_DEPTH_32F, 1)
        
        self.imgMat = cv.CreateMat(img.height, img.width, cv.CV_8UC3)
        cv.Convert(self.img, self.imgMat)
        tStart = time.clock()
        sys.stdout.write('1')
        for y in range(img.height):
            for x in range(img.width):
                self.blueChannel[y,x] = img[y,x][0]
                self.greenChannel[y,x] = img[y,x][1]
                self.redChannel[y,x] = img[y,x][2]
                self.fblueChannel[y,x] = img[y,x][0]
                self.fgreenChannel[y,x] = img[y,x][1]
                self.fredChannel[y,x] = img[y,x][2]
                self.fgrayChannel[y,x] = igray[y,x]
        sys.stdout.write('2')
        tStop = time.clock()
        #print 'initialization: ' + str(tStop - tStart)
        self.imgGray = cv.CreateImage((self.img.width, self.img.height), self.img.depth, 1)
        cv.CvtColor(self.img, self.imgGray, cv.CV_BGR2GRAY)
        self.fourierGray = cv.CreateMat(img.height, img.width, cv.CV_32FC1)
        self.fourierBlue = cv.CreateMat(img.height, img.width, cv.CV_32FC1)
        self.fourierGreen = cv.CreateMat(img.height, img.width, cv.CV_32FC1)
        self.fourierRed = cv.CreateMat(img.height, img.width, cv.CV_32FC1)
        cv.DFT(self.fgrayChannel, self.fourierGray, cv.CV_DXT_FORWARD)
        cv.DFT(self.fblueChannel, self.fourierBlue, cv.CV_DXT_FORWARD)
        cv.DFT(self.fgreenChannel, self.fourierGreen, cv.CV_DXT_FORWARD)
        cv.DFT(self.fredChannel, self.fourierRed, cv.CV_DXT_FORWARD)
        cv.CvtColor(self.img, self.imgGray, cv.CV_BGR2GRAY)
        #Get the Laplace of each image
        self.imgLaplace = cv.CreateImage((img.width, img.height), img.depth, 3)
        self.blueLaplace = cv.CreateImage((img.width, img.height), img.depth, 1)
        self.greenLaplace = cv.CreateImage((img.width, img.height), img.depth, 1)
        self.redLaplace = cv.CreateImage((img.width, img.height), img.depth, 1)
        sys.stdout.write('3')
        if self.aColors:
            self.analyzeColors()
##        tStart = time.clock()
        sys.stdout.write('4')
        if self.aSumLaplace:
            self.sumLaplace()
##        tStop = time.clock()
##        print "sum laplace: " + str(tStop - tStart)
##        tStart = time.clock()
        sys.stdout.write('5')
        if self.aSumCanny:
            self.sumCanny()
##        tStop = time.clock()
##        print 'canny: ' + str(tStop-tStart) 
##        tStart = time.clock()
        sys.stdout.write('6')
        if self.aSumBinLaplace:
            self.sumBinLaplace()
        sys.stdout.write('7')
        if self.aSumFourier:
            self.sumFourier()
        sys.stdout.write('8')
        if self.aSumBinFourier:
            self.sumBinFourier()
        sys.stdout.write('9')
        if self.aSumLonersFourier:
            self.sumLonersFourier()
        sys.stdout.write('0|\n')
        if self.aSumBinLonersFourier:
            self.sumBinLonersFourier()
        #if subdepth > 0:
            #self.getSubImageStats(subdepth)
##        tStop = time.clock()
##        print "sum bin laplace: " + str(tStop - tStart)

    def analyzeColors(self):
        blueMat = cv.CreateMat(self.img.height, self.img.width, cv.CV_8UC1)
        greenMat = cv.CreateMat(self.img.height, self.img.width, cv.CV_8UC1)
        redMat = cv.CreateMat(self.img.height, self.img.width, cv.CV_8UC1)
        cv.Split(self.imgMat, blueMat, greenMat, redMat, None)
        
        self.meanBlue = numpy.mean(blueMat)
        self.meanGreen = numpy.mean(greenMat)
        self.meanRed = numpy.mean(redMat)
        self.medianBlue = numpy.median(blueMat)
        self.medianGreen = numpy.median(greenMat)
        self.medianRed = numpy.median(redMat)

    def sumLaplace(self):
        self.allLaplace = cv.CreateImage((self.img.width, self.img.height), self.img.depth, 3)
        self.blueLaplace = cv.CreateImage((self.img.width, self.img.height),self.img.depth, 1)
        self.greenLaplace = cv.CreateImage((self.img.width, self.img.height), self.img.depth, 1)
        self.redLaplace = cv.CreateImage((self.img.width, self.img.height), self.img.depth, 1)
        cv.Laplace(self.img, self.allLaplace)
        cv.Laplace(self.blueChannel, self.blueLaplace)
        cv.Laplace(self.greenChannel, self.greenLaplace)
        cv.Laplace(self.redChannel, self.redLaplace)
        mat = cv.CreateMat(self.img.height, self.img.width, cv.CV_8UC3)
        cv.Convert(self.allLaplace, mat)
        self.sumLaplaceAll = numpy.sum(mat)
        
        mat = cv.CreateMat(self.img.height, self.img.width, cv.CV_8UC1)
        cv.Convert(self.blueLaplace, mat)
        self.sumLaplaceBlue = numpy.sum(mat)
        
        cv.Convert(self.greenLaplace, mat)
        self.sumLaplaceGreen = numpy.sum(mat)
        
        cv.Convert(self.redLaplace, mat)
        self.sumLaplaceRed = numpy.sum(mat)

    def getCanny(self, img):
        pass

    def lengthCanny(self):
        pass

    def sumCanny(self):
        self.allCanny = cv.CreateImage((self.img.width, self.img.height), self.img.depth, 1)
        self.blueCanny = cv.CreateImage((self.img.width, self.img.height), self.img.depth, 1)
        self.greenCanny = cv.CreateImage((self.img.width, self.img.height), self.img.depth, 1)
        self.redCanny = cv.CreateImage((self.img.width, self.img.height), self.img.depth, 1)
        mat = cv.CreateMat(self.img.height, self.img.width, cv.CV_8UC1)
        self.sumAllCanny = []
        self.sumBlueCanny = []
        self.sumGreenCanny = []
        self.sumRedCanny = []
        if self.norm == 0:
            for i in range(27):
                if i == 0:
                    thresh = 1
                elif i == 26:
                    thresh = 255
                else:
                    thresh = 10 * i
                cv.Canny(self.imgGray, self.allCanny, 1, thresh)
                cv.Convert(self.allCanny, mat)
                self.sumAllCanny.append(numpy.sum(mat))
            
                cv.Canny(self.blueChannel, self.blueCanny, 1, thresh)
                cv.Convert(self.blueCanny, mat)
                self.sumBlueCanny.append(numpy.sum(mat))
            
                cv.Canny(self.greenChannel, self.greenCanny, 1, thresh)
                cv.Convert(self.greenCanny, mat)
                self.sumGreenCanny.append(numpy.sum(mat))
                
                cv.Canny(self.redChannel, self.redCanny, 1, thresh)
                cv.Convert(self.redCanny, mat)
                self.sumRedCanny.append(numpy.sum(mat))
        if self.norm == 1:
            for i in range(27):
                if i == 0:
                    thresh = 1
                elif i == 26:
                    thresh = 255
                else:
                    thresh = 10 * i
                cv.Canny(self.imgGray, self.allCanny, 1, thresh)
                cv.Convert(self.allCanny, mat)
                self.sumAllCanny.append(numpy.sum(mat))
            
                cv.Canny(self.blueChannel, self.blueCanny, 1, thresh)
                cv.Convert(self.blueCanny, mat)
                self.sumBlueCanny.append(numpy.sum(mat))
            
                cv.Canny(self.greenChannel, self.greenCanny, 1, thresh)
                cv.Convert(self.greenCanny, mat)
                self.sumGreenCanny.append(numpy.sum(mat))
                
                cv.Canny(self.redChannel, self.redCanny, 1, thresh)
                cv.Convert(self.redCanny, mat)
                self.sumRedCanny.append(numpy.sum(mat))
        
        

    def getBinLaplace(self, img):
        pass

    def lengthBinLaplace(self):
        pass

    def sumBinLaplace(self):
        self.allBinLaplace = cv.CreateImage((self.img.width, self.img.height), self.allLaplace.depth, 3)
        self.blueBinLaplace = cv.CreateImage((self.img.width, self.img.height), self.blueLaplace.depth, 1)
        self.greenBinLaplace = cv.CreateImage((self.img.width, self.img.height), self.greenLaplace.depth, 1)
        self.redBinLaplace = cv.CreateImage((self.img.width, self.img.height), self.redLaplace.depth, 1)
        #cv.Threshold(self.allLaplace, self.allBinLaplace, 150,255,cv.CV_THRESH_BINARY)
        self.sumBlueBinLaplace = []
        self.sumGreenBinLaplace = []
        self.sumRedBinLaplace = []
        for i in range(27):
            if i == 0:
                thresh = 1
            elif i == 26:
                thresh = 255
            else:
                thresh = 10 * i
            cv.Threshold(self.blueLaplace, self.blueBinLaplace, thresh,255,cv.CV_THRESH_BINARY)
            cv.Threshold(self.greenLaplace, self.greenBinLaplace, thresh,255,cv.CV_THRESH_BINARY)
            cv.Threshold(self.redLaplace, self.redBinLaplace, thresh,255,cv.CV_THRESH_BINARY)

            mat = cv.CreateMat(self.img.height, self.img.width, cv.CV_8UC1)
            cv.Convert(self.blueBinLaplace, mat)
            self.sumBlueBinLaplace.append(numpy.sum(mat))

            cv.Convert(self.greenBinLaplace, mat)
            self.sumGreenBinLaplace.append(numpy.sum(mat))

            cv.Convert(self.redBinLaplace, mat)
            self.sumRedBinLaplace.append(numpy.sum(mat))

    def getCannyLaplace(self, img):
        pass

    def getBinCannyLaplace(self, img):
        pass

    def lengthBinCannyLaplace(Self):
        pass

    def sumBinCannyLaplace(self):
        pass

    def sumFourier(self):
        self.sumFourierGray = numpy.sum(self.fourierGray)
        self.sumFourierBlue = numpy.sum(self.fourierBlue)
        self.sumFourierGreen = numpy.sum(self.fourierGreen)
        self.sumFourierRed = numpy.sum(self.fourierRed)

    def sumBinFourier(self):
        self.binFourierGray = []
        self.binFourierBlue = []
        self.binFourierGreen = []
        self.binFourierRed = []
        self.sumBinFourierGray = []
        self.sumBinFourierBlue = []
        self.sumBinFourierGreen = []
        self.sumBinFourierRed = []
        for i in range(27):
            self.binFourierGray.append(cv.CreateMat(self.img.height, self.img.width, cv.CV_32FC1))
            self.binFourierBlue.append(cv.CreateMat(self.img.height, self.img.width, cv.CV_32FC1))
            self.binFourierGreen.append(cv.CreateMat(self.img.height, self.img.width, cv.CV_32FC1))
            self.binFourierRed.append(cv.CreateMat(self.img.height, self.img.width, cv.CV_32FC1))
        for x in range(self.img.height):
            for y in range(self.img.width):
                for i in range(27):
                    if i == 0:
                        thresh = 1
                    elif i == 26:
                        thresh = 255
                    else:
                        thresh = 10 * i
                    if self.fourierGray[x,y] >= thresh:
                        self.binFourierGray[i][x,y] = 255
                    else:
                        self.binFourierGray[i][x,y] = 0
                    if self.fourierBlue[x,y] >= thresh:
                        self.binFourierBlue[i][x,y] = 255
                    else:
                        self.binFourierBlue[i][x,y] = 0
                    if self.fourierGreen[x,y] >= thresh:
                        self.binFourierGreen[i][x,y] = 255
                    else:
                        self.binFourierGreen[i][x,y] = 0
                    if self.fourierRed[x,y] >= thresh:
                        self.binFourierRed[i][x,y] = 255
                    else:
                        self.binFourierRed[i][x,y] = 0
        for i in range(27):
            self.sumBinFourierGray.append(numpy.sum(self.binFourierGray[i]))
            self.sumBinFourierBlue.append(numpy.sum(self.binFourierBlue[i]))
            self.sumBinFourierGreen.append(numpy.sum(self.binFourierGreen[i]))
            self.sumBinFourierRed.append(numpy.sum(self.binFourierRed[i]))
                        
        for i in range(27):
            if i == 0:
                thresh = 1
            elif i == 26:
                thresh = 255
            else:
                thresh = 10 * i
            #print 'bin fourier ' + str(thresh)
            self.sumBinFourierGray.append(numpy.sum(self.getbinary(self.fourierGray, thresh)))
            self.sumBinFourierBlue.append(numpy.sum(self.getbinary(self.fourierBlue, thresh)))
            self.sumBinFourierGreen.append(numpy.sum(self.getbinary(self.fourierGreen, thresh)))
            self.sumBinFourierRed.append(numpy.sum(self.getbinary(self.fourierRed, thresh)))
            
    def sumLonersFourier(self):
        self.sumLonersFourierGray = []
        self.sumLonersFourierBlue = []
        self.sumLonersFourierGreen = []
        self.sumLonersFourierRed = []
        for i in range(27):
            if i == 0:
                thresh = 1
            elif i == 26:
                thresh = 255
            else:
                thresh = 10 * i
            #print 'loners fourier ' + str(thresh)
            self.sumLonersFourierGray.append(numpy.sum(self.getloners(self.fourierGray, thresh)))
            self.sumLonersFourierBlue.append(numpy.sum(self.getloners(self.fourierBlue, thresh)))
            self.sumLonersFourierGreen.append(numpy.sum(self.getloners(self.fourierGreen, thresh)))
            self.sumLonersFourierRed.append(numpy.sum(self.getloners(self.fourierRed, thresh)))

    def sumBinLonersFourier(self):
        pass
    
    def getSubImageStats(self, depth):
        print 'bad'
        q1 = cv.CreateImage((self.img.width/2, self.img.height/2), self.img.depth, 3)
        q2 = cv.CreateImage((self.img.width/2, self.img.height/2), self.img.depth, 3)
        q3 = cv.CreateImage((self.img.width/2, self.img.height/2), self.img.depth, 3)
        q4 = cv.CreateImage((self.img.width/2, self.img.height/2), self.img.depth, 3)
        n1 = cv.CreateImage((self.img.width/2, self.img.height/2), self.img.depth, 3)
        n2 = cv.CreateImage((self.img.width/2, self.img.height/2), self.img.depth, 3)
        n3 = cv.CreateImage((self.img.width/2, self.img.height/2), self.img.depth, 3)
        n4 = cv.CreateImage((self.img.width/2, self.img.height/2), self.img.depth, 3)
        for y in range(self.img.height):
            for x in range(self.img.width):
                if x < self.img.width/2:
                    if y < self.img.height/2:
                        q1[y,x] = self.img[y,x]
                        n1[y,x] = self.getNorm(self.img[y,x])
                    else:
                        q2[y - (self.img.height/2),x] = self.img[y,x]
                        n2[y - (self.img.height/2),x] = self.getNorm(self.img[y,x])
                else:
                    if y < self.img.height/2:
                        q3[y, x - (self.img.width/2)] = self.img[y,x]
                        n3[y, x - (self.img.width/2)] = self.getNorm(self.img[y,x])
                    else:
                        q4[y - (self.img.height/2), x - (self.img.width/2)] = self.img[y,x]
                        n4[y - (self.img.height/2), x - (self.img.width/2)] = self.getNorm(self.img[y,x])
        a1 = Analysis(q1,0,depth-1)
        a2 = Analysis(q2,0,depth-1)
        a3 = Analysis(q3,0,depth-1)
        a4 = Analysis(q4,0,depth-1)

        self.medianMeanBlue = numpy.median([a1.meanBlue, a2.meanBlue, a3.meanBlue, a4.meanBlue])
        self.medianMeanGreen = numpy.median([a1.meanGreen, a2.meanGreen, a3.meanGreen, a4.meanGreen])
        self.medianMeanRed = numpy.median([a1.meanRed, a2.meanRed, a3.meanRed, a4.meanRed])
        self.medianMedianBlue = numpy.median([a1.medianBlue, a2.medianBlue, a3.medianBlue, a4.medianBlue])
        self.medianMedianGreen = numpy.median([a1.medianGreen, a2.medianGreen, a3.medianGreen, a4.medianGreen])
        self.medianMedianRed = numpy.median([a1.medianRed, a2.medianRed, a3.medianRed, a4.medianRed])
##
##        self.normmedianMeanBlue = numpy.median([n1.meanBlue, n2.meanBlue, n3.meanBlue, n4.meanBlue])
##        self.normmedianMeanGreen = numpy.median([n1.meanGreen, n2.meanGreen, n3.meanGreen, n4.meanGreen])
##        self.normmedianMeanred = numpy.median([n1.meanRed, n2.meanRed, n3.meanRed, n4.meanRed])
##        self.normmedianMedianBlue = numpy.median([n1.medianBlue, n2.medianBlue, n3.medianBlue, n4.medianBlue])
##        self.normmedianMedianGreen = numpy.median([n1.medianGreen, n2.medianGreen, n3.medianGreen, n4.medianGreen])
##        self.normmedianMedianRed = numpy.median([n1.medianRed, n2.medianRed, n3.medianRed, n4.medianRed])

        self.medianSumLaplaceAll = numpy.median([a1.sumLaplaceAll, a2.sumLaplaceAll, a3.sumLaplaceAll, a4.sumLaplaceAll])
        self.medianSumLaplaceBlue = numpy.median([a1.sumLaplaceBlue, a2.sumLaplaceBlue, a3.sumLaplaceBlue, a4.sumLaplaceBlue])
        self.medianSumLaplaceGreen = numpy.median([a1.sumLaplaceGreen, a2.sumLaplaceGreen, a3.sumLaplaceGreen, a4.sumLaplaceGreen])
        self.medianSumLaplaceRed = numpy.median([a1.sumLaplaceRed, a2.sumLaplaceRed, a3.sumLaplaceRed, a4.sumLaplaceRed])
##
##        self.normmedianSumLaplaceAll = numpy.median([n1.sumLaplaceAll, n2.sumLaplaceAll, n3.sumLaplaceAll, n4.sumLaplaceAll])
##        self.normmedianSumLaplaceBlue = numpy.median([n1.sumLaplaceBlue, n2.sumLaplaceBlue, n3.sumLaplaceBlue, n4.sumLaplaceBlue])
##        self.normmedianSumLaplaceGreen = numpy.median([n1.sumLaplaceGreen, n2.sumLaplaceGreen, n3.sumLaplaceGreen, n4.sumLaplaceGreen])
##        self.normmedianSumLaplaceRed = numpy.median([n1.sumLaplaceRed, n2.sumLaplaceRed, n3.sumLaplaceRed, n4.sumLaplaceRed])
        self.medianSumAllCanny = []
        self.medianSumBlueCanny = []
        self.medianSumGreenCanny = []
        self.medianSumRedCanny = []
        if self.norm == 0:
            for i in range(27):
                self.medianSumAllCanny.append(numpy.median([a1.sumAllCanny[i], a2.sumAllCanny[i], a3.sumAllCanny[i], a4.sumAllCanny[i]]))
                self.medianSumBlueCanny.append(numpy.median([a1.sumBlueCanny[i], a2.sumBlueCanny[i], a3.sumBlueCanny[i], a4.sumBlueCanny[i]]))
                self.medianSumGreenCanny.append(numpy.median([a1.sumGreenCanny[i], a2.sumGreenCanny[i], a3.sumGreenCanny[i], a4.sumGreenCanny[i]]))
                self.medianSumRedCanny.append(numpy.median([a1.sumRedCanny[i], a2.sumRedCanny[i], a3.sumRedCanny[i], a4.sumRedCanny[i]]))

##                self.normmedianSumAllCanny.append(numpy.median([n1.sumAllCanny[i], n2.sumAllCanny[i], n3.sumAllCanny[i], n4.sumAllCanny[i]]))
##                self.normmedianSumBlueCanny.append(numpy.median([n1.sumBlueCanny[i], n2.sumBlueCanny[i], n3.sumBlueCanny[i], n4.sumBlueCanny[i]]))
##                self.normmedianSumGreenCanny.append(numpy.median([n1.sumGreenCanny[i], n2.sumGreenCanny[i], n3.sumGreenCanny[i], n4.sumGreenCanny[i]]))
##                self.normmedianSumRedCanny.append(numpy.median([n1.sumRedCanny[i], n2.sumRedCanny[i], n3.sumRedCanny[i], n4.sumRedCanny[i]]))
                
        if self.norm == 1:
            for i in range(27):
                self.medianSumAllCanny.append(numpy.median([a1.sumAllCanny[i], a2.sumAllCanny[i], a3.sumAllCanny[i], a4.sumAllCanny[i]]))
                self.medianSumBlueCanny.append(numpy.median([a1.sumBlueCanny[i], a2.sumBlueCanny[i], a3.sumBlueCanny[i], a4.sumBlueCanny[i]]))
                self.medianSumGreenCanny.append(numpy.median([a1.sumGreenCanny[i], a2.sumGreenCanny[i], a3.sumGreenCanny[i], a4.sumGreenCanny[i]]))
                self.medianSumRedCanny.append(numpy.median([a1.sumRedCanny[i], a2.sumRedCanny[i], a3.sumRedCanny[i], a4.sumRedCanny[i]]))

##                self.normmedianSumAllCanny.append(numpy.median([n1.sumAllCanny[i], n2.sumAllCanny[i], n3.sumAllCanny[i], n4.sumAllCanny[i]]))
##                self.normmedianSumBlueCanny.append(numpy.median([n1.sumBlueCanny[i], n2.sumBlueCanny[i], n3.sumBlueCanny[i], n4.sumBlueCanny[i]]))
##                self.normmedianSumGreenCanny.append(numpy.median([n1.sumGreenCanny[i], n2.sumGreenCanny[i], n3.sumGreenCanny[i], n4.sumGreenCanny[i]]))
##                self.normmedianSumRedCanny.append(numpy.median([n1.sumRedCanny[i], n2.sumRedCanny[i], n3.sumRedCanny[i], n4.sumRedCanny[i]]))

        
            
    def getNorm(self, pixel):
        s = pixel[0] + pixel[1] + pixel[2]
        out = []
        out.append((pixel[0]/s) * 255)
        out.append((pixel[1]/s) * 255)
        out.append((pixel[2]/s) * 255)
        return out

    def getcolumnform(self):
        #form =
        #self, column name, thresh
        col = []
        if self.aColors:
            col.append((self, 'meanBlue', 0))
            col.append((self, 'meanGreen', 0))
            col.append((self, 'meanRed', 0))
            col.append((self, 'medianBlue', 0))
            col.append((self, 'medianGreen', 0))
            col.append((self, 'medianRed', 0))
        if self.aSumLaplace:
            col.append((self, 'sumLaplaceAll', 0))
            col.append((self, 'sumLaplaceBlue', 0))
            col.append((self, 'sumLaplaceGreen', 0))
            col.append((self, 'sumLaplaceRed', 0))
        if self.aSumCanny:
            for i in range(27):
                col.append((self, 'sumAllCanny', i))
            for i in range(27):
                col.append((self, 'sumBlueCanny', i))
            for i in range(27):
                col.append((self, 'sumGreenCanny', i))
            for i in range(27):
                col.append((self, 'sumRedCanny', i))
        if self.aSumBinLaplace:
            for i in range(27):
                col.append((self, 'sumBlueBinLaplace', i))
            for i in range(27):
                col.append((self, 'sumGreenBinlaplace', i))
            for i in range(27):
                col.append((self, 'sumRedBinLaplace', i))
        if self.aSumFourier:
            col.append((self, 'sumFourierGray', 0))
            col.append((self, 'sumFourierBlue', 0))
            col.append((self, 'sumFourierGreen', 0))
            col.append((self, 'sumFourierRed', 0))
        if self.aSumBinFourier:
            for i in range(27):
                col.append((self, 'sumBinFourierGray', i))
            for i in range(27):
                col.append((self, 'sumBinFourierBlue', i))
            for i in range(27):
                col.append((self, 'sumBinFourierGreen', i))
            for i in range(27):
                col.append((self, 'sumBinFourierRed', i))
        if self.aSumLonersFourier:
            for i in range(27):
                col.append((self, 'sumLonersFourierGray', i))
            for i in range(27):
                col.append((self, 'sumLonersFourierBlue', i))
            for i in range(27):
                col.append((self, 'sumLonersFourierGreen', i))
            for i in range(27):
                col.append((self, 'sumLonersFourierRed', i))
        return col
        

    def getvar(self, varname, thresh = 0):
        if varname == 'meanBlue':
            return self.meanBlue
        if varname == 'meanGreen':
            return self.meanGreen
        if varname == 'meanRed':
            return self.meanRed
        if varname == 'medianBlue':
            return self.medianBlue
        if varname == 'medianGreen':
            return self.medianGreen
        if varname == 'medianRed':
            return self.medianRed
        if varname == 'sumLaplaceAll':
            return self.sumLaplaceAll
        if varname == 'sumLaplaceBlue':
            return self.sumLaplaceBlue
        if varname == 'sumLaplaceGreen':
            return self.sumLaplaceGreen
        if varname == 'sumLaplaceRed':
            return self.sumLaplaceRed
        if varname == 'sumAllCanny':
            return self.sumAllCanny[thresh]
        if varname == 'sumBlueCanny':
            return self.sumBlueCanny[thresh]
        if varname == 'sumGreenCanny':
            return self.sumGreenCanny[thresh]
        if varname == 'sumRedCanny':
            return self.sumRedCanny[thresh]
        if varname == 'sumBlueBinLaplace':
            return self.sumBlueBinLaplace[thresh]
        if varname == 'sumGreenBinLaplace':
            return self.sumGreenBinLaplace[thresh]
        if varname == 'sumRedBinLaplace':
            return self.sumRedBinLaplace[thresh]
        if varname == 'sumFourierGray':
            return self.sumFourierGray
        if varname == 'sumFourierBlue':
            return self.sumFourierBlue
        if varname == 'sumFourierGreen':
            return self.sumFourierGreen
        if varname == 'sumFourierRed':
            return self.sumFourierRed
        if varname == 'sumBinFourierGray':
            return self.sumBinFourierGray[thresh]
        if varname == 'sumBinFourierBlue':
            return self.sumBinFourierBlue[thresh]
        if varname == 'sumBinFourierGreen':
            return self.sumBinFourierGreen[thresh]
        if varname == 'sumBinFourierRed':
            return self.sumBinFourierRed[thresh]
        if varname == 'sumLonersFourierGray':
            return self.sumLonersFourierGray[thresh]
        if varname == 'sumLonersFourierBlue':
            return self.sumLonersFourierBlue[thresh]
        if varname == 'sumLonersFourierGreen':
            return self.sumLonersFourierGreen[thresh]
        if varname == 'sumLonersFourierRed':
            return self.sumLonersFourierRed[thresh]
        

    def copy(self, img):
        result = cv.CreateImage((img.width,img.height), cv.IPL_DEPTH_32F, 1)
        for i in range(img.height):
            for j in range(img.width):
                result[i,j] = img[i,j]
        return result
    def getbinary(self, img, thresh = 255):
        result = cv.CreateImage((img.width, img.height), cv.IPL_DEPTH_32F, 1)
        for i in range(img.height):
            for j in range(img.width):
                if img[i,j] >= thresh:
                    result[i,j] = 255
                else:
                    result[i,j] = 0
        return result
    def getsinglelonerpixel(self, img, i, j, thresh = 255):
        count = 0
        for x in range(-1,2):
            for y in range(-1,2):
                ei = i+x
                ej = y+j
                if ei < 0 or ei >= img.height or ej < 0 or ej >= img.width:
                    pass
                else:
                    if img[ei,ej] >= thresh:
                        count+=1
        return count
    def getloners(self, img, thresh=255):
        result = cv.CreateImage((img.width, img.height), cv.IPL_DEPTH_32F, 1)
        for i in range(img.height):
            for j in range(img.width):
                c = self.getsinglelonerpixel(img, i, j)
                if c <= 1:
                    result[i,j] = 255
                else:
                    result[i,j] = 0
        return result
