'''
Author: han wu 
Date: 2021-08-30 21:43:21
LastEditTime: 2021-09-21 21:19:08
LastEditors: your name
Description: 
FilePath: /FastApiDemo/tutorial/chapter05.py
~~~~~~~~~吼吼吼~~~~~~~~~~
'''

from typing import Optional,List,Dict
from fastapi import APIRouter, Depends, Header, HTTPException, Request
from fastapi.responses import Response,HTMLResponse
import orjson

app05 = APIRouter()


def common_depends(q: Optional[str] = None, page: int = 1, limit: int = 100):
    return {"q": q, "page": page, "imit": "limit"}


@app05.get('/depends01')
async def defpendency01(commons: dict = Depends(common_depends)):
    return commons


@app05.get('/depends02')
async def defpendency02(commons: dict = Depends(common_depends)):
    return commons

#  类 作为 依赖项
fake_user_db = [{"itme": "1", "name": "yanzu"}, {"item": "2", "name": "wuhan"},
                {"item": "3", "name": "yuyan"}]


class CommonQueryParams:
    def __init__(self, q: Optional[str] = None, page: int = 1, limit: int = 100):
        self.q = q
        self.page = page
        self.limit = limit
@app05.get('/class_and_depends')
# async def class_depends(commons: CommonQueryParams = Depends(CommonQueryParams)):
# async def class_depends(commons: CommonQueryParams()):
async def class_depends(commons = Depends(CommonQueryParams)):
    response = {}
    if commons.q:
        response.update({"q":commons.q})
    items = fake_user_db[commons.page : commons.page + commons.limit] 
    response.update({"items":items})
    return response
        
# 子依赖

def query(q: Optional[str] = None):
    return q
    
    
def sub_query(q: str = Depends(query), last_query: Optional[str] = None):
    if last_query:
        return last_query
    return q

@app05.get('/sub_query_test')
async def test_sub_query(final_query: str = Depends(sub_query, use_cache=True)):
    return {"final_query": final_query}

# 路径参数中添加依赖

def verify_token(x_token: str = Header(...)):
    if x_token != "fake_x_token":
        raise HTTPException(status_code=400, detail="你输入的这个token就是不对得！")
    return x_token

def verify_key(x_key: str = Header(...)):
    if x_key != "fake_x_token":
        raise HTTPException(status_code=400, detail="你输入的这个key就是不对得！")
    return x_key

@app05.get('/path_def_verify',dependencies=[Depends(verify_token),Depends(verify_key)])
async def path_def_verify():
    return [{"user01":"user01","user02":"user02"}]

# Request
@app05.get('/girl/{user_id}')
async def read_girl(user_id: str, request: Request):
    header = request.headers
    method = request.method
    cookies = request.cookies
    query_params = request.query_params
    # ↓ 此时加入在url中没有拼接参数的话，那么就不会有内容返回
    return {"name": query_params.get("name"), "age": query_params.get("age"), "hobby": query_params.getlist("hobby"),"method":method,"header":header,"cookie":cookies}

# Response
# http://127.0.0.1:7777/chapter05/resp_girl/user_id=1?name=2&age=2&hobby=1
@app05.get('/resp_girl/{user_id}')
async def read_girl_response(user_id: str, request: Request):
    query_params = request.query_params
    data = {"name":query_params.get("name"), "age": query_params.get("age"), "hobby": query_params.getlist("hobby")}

    # 实例化一个Response对象
    response = Response(
        orjson.dumps(data),
        201,
        {"Token":"xxx"},
        "application/json"
    )
    return response

# 自定义 Response响应类型
@app05.get('/index')
async def index():
    response1 = HTMLResponse("<h1>Hello World!</h1>")
    response2 = Response("<h1>你好呀</h1>", media_type="text/html")
    # 以上两者是等价的，在 HTMLResponse 中会自动将 media_type 设置成 text/html
    return response1

# 使用request对象返回
@app05.get("/request_girl/{user_id}")
async def request_girl(user_id, request: Request):
    q = request.query_params.get('q')
    data: Dict = await request.json()
    data.update({"user_id":user_id, "q":q})
    return data