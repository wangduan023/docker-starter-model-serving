import json
from paddle.fluid.core import PaddleTensor
from paddle.fluid.core import PaddleDType
from paddle.fluid.core import PaddleBuf

class ParmsItem(object):

    def __init__(self, name,shape_size,dtype,data):
        self.name = name
        self.shape_size = shape_size
        self.dtype = dtype
        self.data = data
        self.list = [PaddleDType.FLOAT32, PaddleDType.INT64, PaddleDType.INT32]
        pass

    def copyToTensor(self,batch_size):
        tensor = PaddleTensor()
        tensor.name = self.name
        tensor.shape = [batch_size, self.shape_size]
        tensor.dtype =  self.list[self.dtype]
        tensor.data = PaddleBuf(self.data)
        return tensor
