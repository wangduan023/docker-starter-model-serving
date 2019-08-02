import sys
import os.path
import aiohttp
import asyncio

class Update(object):
    def __init__(self):
        self.update_net_url =  ""
        self.model_base_path = "app/models/"
        self.model_name = "fit_a_line"
        pass

    def get_model_name(self):
        return self.model_base_path+self.model_name

    #设置网络更新地址    
    def get_net_url(self):
        return self.update_net_url

    def set_model_base_path(self,model_base_path):
        self.model_base_path = model_base_path  

    def set_model_default_name(self,model_name):
        self.model_name = model_name;

    #获取版本
    async def get_version(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.update_net_url) as response:
                data = await response.read();
                return data
    #下载文件
    async def download_file(self):
        ver = await self.get_version()
        model_url = ver.model_url
        model_version = ver.model_version
        path = model_base_path+model_version

        if os.path.exists(path): return
        async with aiohttp.ClientSession() as session:
            async with session.get(model_url) as response:
                data = await response.read()
                with open(path, 'wb') as f:
                    f.write(data)
                    self.model_name = model_version
                    return self.model_name