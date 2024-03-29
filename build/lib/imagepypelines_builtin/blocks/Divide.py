# @Email: jmaggio14@gmail.com
# @Website: https://www.imagepypelines.org/
# @License: https://github.com/jmaggio14/imagepypelines/blob/master/LICENSE
# @github: https://github.com/jmaggio14/imagepypelines
#
# Copyright (c) 2018-2019 Jeff Maggio, Nathan Dileas, Ryan Hartzell
#
from imagepypelines import SimpleBlock
from imagepypelines import ArrayType
from imagepypelines import Same
import numpy as np

class Divide(SimpleBlock):
    def __init__(self,divisor):
        assert isinstance(divisor,(int,float,np.ndarray))
        self.divisor = divisor
        io_map = {
                    ArrayType():Same(),
                    int:float,
                    float:float
                    }
        super(Divide,self).__init__(io_map)

    def process(self, datum):
        return datum / self.divisor
