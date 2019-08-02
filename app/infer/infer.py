from paddle.fluid.core import PaddleBuf
from paddle.fluid.core import PaddleDType
from paddle.fluid.core import PaddleTensor
from paddle.fluid.core import AnalysisConfig
from paddle.fluid.core import create_paddle_predictor

class Infer(object):
    def __init__(self, *args, **kwargs):
        self.predictor =  None
        self.histroy = []
        return super().__init__(*args, **kwargs)

    def load_model(self, model_dir,roll_back=False):
        print("load_model==>",model_dir)
        config = AnalysisConfig(model_dir)
        #不启动cpu
        config.disable_gpu()
        #把老的模型留存
        if self.predictor and roll_back:
            self.histroy.push(self.predictor)
        #创建预测
        self.predictor = create_paddle_predictor(config)

        return self.predictor

    def run(self,inputs):
        if self.predictor:
            return self.predictor.run(inputs)
        else:
            return 'model init'

    #预测参数 可以由子类重新
    def fake_input(self,batch_size):
        image = PaddleTensor()
        image.name = "x"
        image.shape = [batch_size, 13]
        image.dtype = PaddleDType.FLOAT32
        image.data = PaddleBuf(
            [ 0.42616305, -0.11363637,  0.25525004, -0.06916996,  0.28457806, -0.14440207,
            0.17327599, -0.19893268,  0.62828666,  0.49191383,  0.18558154, -0.06862179,
            0.40637243])
        return [image]
