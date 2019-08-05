import sys
import json
import os.path
import aiohttp
import asyncio
import uvicorn
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

from paddle.fluid.core import PaddleDType

#paddle
from infer.infer import Infer

from infer.update  import Update

from infer.parms import ParmsItem

#是否采用网络更新
is_update = False;
#模型的基础路径
model_base_path = 'app/models/'
#这个名字可以从网络取出名字
model_name = 'fit_a_line'

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))

_infer =  Infer()
_update = Update()
#构建预测infer

async def setup_learner():
    # 如果可以更新模型都需要从网络加载 网络加载模型
    if is_update:
        await _update.download_file()
    try:
        learn = _infer.load_model(_update.get_model_name())
        return learn
    except RuntimeError as e:
        raise e


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

#json转换为json2parms
def json2parms(p):
    return ParmsItem(p['name'], p['shape_size'],p['dtype'],p['data'])
#预测结果返回 json转换
def paddle2dict(tensor):
    return {'name': tensor.name,
            'data': type2data(tensor)}
#根据类型得出数据
def type2data(tensor):
    dtype = tensor.dtype
    data = tensor.data 
    if dtype==PaddleDType.FLOAT32:
       return data.float_data()
    if dtype==PaddleDType.INT32:
       return data.int_data()
    if dtype==PaddleDType.INT64:
       return data.int_data() 
    else:
       return "unkown"               
#加载首页
@app.route('/')
async def homepage(request):
    return HTMLResponse('欢迎使用'+ _update.get_net_url())

#模型的更新
@app.route('/update', methods=['POST','GET'])
async def update(request):
    #下载更新模型
    learn = setup_learner()
    return JSONResponse({'result': str('更新完毕')})

#模型参数预测接收参数为json
@app.route('/infer', methods=['POST'])
async def update(request):
    # 预测图片传递方式
    # img_data = await request.form()
    # img_bytes = await (img_data['file'].read())
    # img = open_image(BytesIO(img_bytes))
    # parms[{'name':x,'shape_size':10,'dtype':0|1|2,'data':1,2,3|[1,2,3,4,5]},ParmsItem]
    form = await request.form()
    p_json = form['parms']
    p_batch = form["batch"]
    parms = json.loads(p_json,default=json2parms)
    # 运行预测引擎得到结果，返回值是一个PaddleTensor的list
    outputs = _infer.run(_infer.fake_input(p_batch,[parms]))
    return JSONResponse({'result': json.dumps(outputs,default=paddle2dict)})

#模型分析预测
@app.route('/analyze', methods=['POST','GET'])
async def analyze(request):
    # img_data = await request.form()
    # img_bytes = await (img_data['file'].read())
    # img = open_image(BytesIO(img_bytes))
    # prediction = learn.predict(img)[0]
    #   FLOAT32,
    #   INT64,
    #   INT32,
    data =   [ 0.42616305, -0.11363637,  0.25525004, -0.06916996,  0.28457806, -0.14440207,
               0.17327599, -0.19893268,  0.62828666,  0.49191383,  0.18558154, -0.06862179,
               0.40637243]   
    #dtype   FLOAT32 0    INT64 1    INT32 2  
    parm =  ParmsItem("x",13,0,data)
    # 运行预测引擎得到结果，返回值是一个PaddleTensor的list
    outputs = _infer.run(_infer.fake_input(5,[parm]))
    return JSONResponse({'result': json.dumps(outputs,default=paddle2dict)})


#启动程序
if __name__ == '__main__':
    if len(sys.argv)>3:
        update_net_url = sys.argv[2]
        is_update = sys.argv[3]=="1"
        _update.set_update_net_url(update_net_url)
        _update.set_model_base_path(model_base_path)
        _update.set_model_default_name(model_name)
    # uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
