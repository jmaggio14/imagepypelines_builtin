# @Email: jmaggio14@gmail.com
# @Website: https://www.imagepypelines.org/
# @License: https://github.com/jmaggio14/imagepypelines/blob/master/LICENSE
# @github: https://github.com/jmaggio14/imagepypelines
#
# Copyright (c) 2018-2019 Jeff Maggio, Nathan Dileas, Ryan Hartzell
from imagepypelines import SimpleBlock
from imagepypelines import ArrayType
import numpy as np
from imagepypelines import import_opencv
cv2 = import_opencv()

class FFT(SimpleBlock):
    """Block to calculate a fast fourier transform on input imagery

    Attributes:

        io_map(IoMap): object that maps inputs to this block to outputs
        name(str): unique name for this block
        requires_training(bool): whether or not this block will require
            training
        trained(bool): whether or not this block has been trained, True
            by default if requires_training = False
        logger(ip.ImagepypelinesLogger): logger for this block,
            registered to 'name'

    """
    def __init__(self):
        io_map = {ArrayType([None,None]):ArrayType([None,None]),
                    ArrayType([None,None,None]):ArrayType([None,None,None]),
                    }
        super(FFT,self).__init__(io_map, requires_training=False)

    def process(self,datum):
        """calculates a fast-fourier transform on an input image

        Args:
            datum (np.ndarray): image numpy array to take fourier transform of

        Returns:
            fft(np.ndarray): zero-centered fourier transform

        """

        if len(datum.shape) == 2:

            fft = np.fft.fft2(datum)
            fft = np.fft.fftshift(fft)

        if len(datum.shape) == 3:

            fft = []

            for band in range(0,datum.shape[-1]):

                F = np.fft.fft2(datum[:,:,band])
                F = np.fft.fftshift(F)
                fft.append(F)

            fft = np.dstack(fft)

        return fft
