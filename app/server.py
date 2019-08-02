import sys
import os.path
import aiohttp
import asyncio
import uvicorn
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
#paddle
from infer.infer import Infer
from infer.update  import Update

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

#模型分析预测
@app.route('/analyze', methods=['POST','GET'])
async def analyze(request):
    # img_data = await request.form()
    # img_bytes = await (img_data['file'].read())
    # img = open_image(BytesIO(img_bytes))
    # prediction = learn.predict(img)[0]
    outputs = _infer.run(_infer.fake_input(5))
    output = outputs[0]
    output_data = output.data.float_data()
    return JSONResponse({'result': str(output_data)})


#启动程序
if __name__ == '__main__':
    if len(sys.argv)>3:
        update_net_url = sys.argv[2]
        is_update = sys.argv[3]=="1"
        _update.set_update_net_url(update_net_url)
        _update.set_model_base_path(model_base_path)
        _update.set_model_default_name(model_name)

    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
