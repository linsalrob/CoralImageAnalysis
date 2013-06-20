import numpy

class FFT:
    '''A class to handle the fft calls for image analysis'''

    def fft(self, img):
        '''Calculate the fast Fourier transformation of an image. This requires a 2D image (e.g. greyscale or single color channel.

        fft = fft(img)
        '''
        if (len(img.shape) != 2):
            sys.stderr.write("The image passed to fft is not a 2D image. Please refactor")
            return

        return numpy.fft.fft2(img)

    def energy(self, img):
        '''The energy in the image is calculated as the square root of the sum of squares of the magnitude of the fft (the real part). 

        Returns a single integer for the image. '''

        return numpy.sqrt(numpy.sum(numpy.abs(fft(img)) ** 2)
