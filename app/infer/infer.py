from paddle.fluid.core import PaddleBuf
from paddle.fluid.core import PaddleDType
from paddle.fluid.core import PaddleTensor
from paddle.fluid.core import AnalysisConfig
from paddle.fluid.core import create_paddle_predictor
from infer.parms import ParmsItem


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

    #预测参数 可以由子类重写
    def fake_input(self,batch_size,parms):
        return list(map(lambda item: item.copyToTensor(batch_size),parms))
