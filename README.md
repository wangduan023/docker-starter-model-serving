本项目复制于 [fast.ai](https://www.fast.ai) models on [Render](https://render.com)

开发环境在mac,部署环境Ubuntu.

模型文件保存在app/models下

预测代码文件在 app/infer/infer.py

预测接口 api  http://host:5000/infer 

post 传递参数 'parms'==> [{'name':x,'shape_size':10,'dtype':0|1|2,'data':1,2,3|[1,2,3,4,5]},ParmsItem] ,'batch,=> 个数


# 本地docker 测试:

1.克隆下载本仓库 , docker-starter-model-serving, 进入程序目录 docker build . 
2.docker run  -p 5000:5000 "image-name-you-want-to-run", e.g. e76782de76a6
3.打开 localhost:5000 检查预测程序 http://127.0.0.1:5000/analyze .
4. 替换models 中模型都开始自己预测   

# 本地测试:
1.克隆下载本仓库 , docker-starter-model-serving, 进入程序目录 python app/server.py serve
