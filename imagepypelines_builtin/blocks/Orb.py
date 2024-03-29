# @Email: jmaggio14@gmail.com
# @Website: https://www.imagepypelines.org/
# @License: https://github.com/jmaggio14/imagepypelines/blob/master/LICENSE
# @github: https://github.com/jmaggio14/imagepypelines
#
# Copyright (c) 2018-2019 Jeff Maggio, Nathan Dileas, Ryan Hartzell
from imagepypelines import SimpleBlock
from imagepypelines import ArrayType
from imagepypelines import import_opencv
cv2 = import_opencv()
import numpy as np

class Orb(SimpleBlock):
    """Block to calculate ORB features upon input grayscale imagery

    Args:
        n_keypoints(int): maximum number of keypoints to detect

    Attributes:
        n_keypoints(int): maximum number of keypoints to detect
        orb(cv2.ORB): orb computation object from opencv

        io_map(IoMap): object that maps inputs to this block to outputs
        name(str): unique name for this block
        requires_training(bool): whether or not this block will require
            training
        trained(bool): whether or not this block has been trained, True
            by default if requires_training = False
        logger(ip.ImagepypelinesLogger): logger for this block,
            registered to 'name'

    """
    def __init__(self,n_keypoints=100):
        if not isinstance(n_keypoints,(int,float)):
            error_msg = "'n_keypoints' must be int"
            self.logger.error(error_msg)
            raise TypeError(error_msg)

        self.n_keypoints = int(n_keypoints)
        self.orb = cv2.ORB_create(self.n_keypoints)

        io_map = {ArrayType([None,None]) : ArrayType([self.n_keypoints,32])}
        super(Orb,self).__init__(io_map, requires_training=False)

    def process(self,datum):
        """calculates descriptors on a single grascale image (height,width)

        If there are not enough keypoints calculated to populate the output
        array, the descriptor vectors will be replaced with zeros

        Args:
            datum (np.ndarray): image numpy array to process
                shape = (width,bands)

        Returns:
            descriptors(np.ndarray): 2D array of ORB descriptors
                shape = (n_keypoints,32)

        """
        _,des = self.orb.detectAndCompute(datum,None)


        #JM:
        # return masked values in case there aren't enough keypoints in the image
        # this is to make sure that stacking systems later don't break
        if des is None:
            zeros = np.zeros( (self.n_keypoints,32) )
            mask = np.ones(zeros.shape).astype(int)
            des = np.ma.masked_array(zeros,mask)
        elif des.shape[0] < self.n_keypoints:
            zeros = np.zeros( (self.n_keypoints-des.shape[0],32) )
            mask = np.vstack( ( np.zeros((des.shape[0],32)),np.ones(zeros.shape)) )
            des = np.ma.masked_array( np.vstack((des,zeros)),mask )

        # JM: DEBUG #TEMP
        # for some reason, maximum number of features set in ORB doesn't
        # seem to operating correctly -- we get 16 keypoints for sparse_checkerboard
        # when 10 is set as out maximum
        # AS A TEMPORARY FIX, I am cutting out descriptors past the maximum
        # so other parts of the pipeline can be test
        if des.shape[0] > self.n_keypoints:
            des = des[:self.n_keypoints,:]
        # END DEBUG, END TEMP
        return des

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['orb']
        return state

    def __setstate__(self, state):
        self.orb = cv2.ORB_create(self.n_keypoints)
