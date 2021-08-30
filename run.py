# 主程序文件

from fastapi import FastAPI
import uvicorn
from tutorial import app03, app04, app05, app06, app07, app08


app = FastAPI()

app.include_router(app03, prefix='/chapter03', tags=['第三章 请求参数和验证'])
app.include_router(app04, prefix='/chapter04', tags=['第四章 响应处理和FastApi配置']) 
app.include_router(app05, prefix='/chapter05', tags=['第五章 FastApi依赖注入系统'])
app.include_router(app06, prefix='/chapter06', tags=['第六章 认证和授权'])
app.include_router(app07, prefix='/chapter07', tags=['第七章 FatApi的数据库操作和多应用的目录结构设计'])
app.include_router(app08, prefix='/chapter08', tags=['第八章 中间件，CORS，后台任务，测试用例'])


if __name__ == '__main__':
    uvicorn.run('run:app', host='0.0.0.0', port=7777, reload=True,debug=True,workers=1)
    # workers ： 进程数量
