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

class Flatten(SimpleBlock):
    def __init__(self):
        self.term = term
        io_map = {ArrayType():ArrayType([None])}
        super(Flatten,self).__init__(io_map)

    def process(self, datum):
        return datum.flatten()
