'''
Author: han wu 
Date: 2021-08-30 21:43:21
LastEditTime: 2021-09-21 20:51:02
LastEditors: your name
Description: 
FilePath: /FastApiDemo/tutorial/chapter05.py
~~~~~~~~~吼吼吼~~~~~~~~~~
'''

from typing import Optional
from fastapi import APIRouter, Depends

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