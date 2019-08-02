import sys
import aiohttp
import asyncio
import uvicorn
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
#paddle
from paddle.fluid.core import PaddleBuf
from paddle.fluid.core import PaddleDType
from paddle.fluid.core import PaddleTensor
from paddle.fluid.core import AnalysisConfig
from paddle.fluid.core import create_paddle_predictor

#下载更新模型
export_file_url = 'https://www.345keji.com'
export_file_name = 'fit_a_line'

classes = ['beach', 'denseresidential', 'golfcourse']
path = 'app/models/fit_a_line'

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))


async def download_file(url, dest):
    print("download_file",url,dest)
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f:
                f.write(data)

#构建预测infer
def load_learner(model_dir,export_file_name):

    config = AnalysisConfig('app/models/fit_a_line')
    #不启动cpu
    config.disable_gpu()
    #创建预测
    return create_paddle_predictor(config)

#创建预测参数
def fake_input(batch_size):
    image = PaddleTensor()
    image.name = "x"
    image.shape = [batch_size, 13]
    image.dtype = PaddleDType.FLOAT32
    image.data = PaddleBuf(
        [ 0.42616305, -0.11363637,  0.25525004, -0.06916996,  0.28457806, -0.14440207,
        0.17327599, -0.19893268,  0.62828666,  0.49191383,  0.18558154, -0.06862179,
        0.40637243])
    return [image]

async def setup_learner():
    # await download_file(export_file_url, path / export_file_name)
    try:
        learn = load_learner(path, export_file_name)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

#加载首页
@app.route('/')
async def homepage(request):
    return HTMLResponse('欢迎使用'+export_file_url)

#模型的更新
@app.route('/update', methods=['POST','GET'])
async def update(request):
    #下载更新模型
    learn = setup_learner()
    return JSONResponse({'result': str('更新完毕')})

#模型分析预测
@app.route('/analyze', methods=['POST','GET'])
async def analyze(request):
    # img_data = await request.form()
    # img_bytes = await (img_data['file'].read())
    # img = open_image(BytesIO(img_bytes))
    # prediction = learn.predict(img)[0]
    inputs = fake_input(5)
    outputs = learn.run(inputs)
    output = outputs[0]
    output_data = output.data.float_data()
    return JSONResponse({'result': str(output_data)})


#启动程序
if __name__ == '__main__':
    if len(sys.argv)>2:
        export_file_url = sys.argv[2]
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
