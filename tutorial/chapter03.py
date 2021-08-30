from enum import Enum
from fastapi import APIRouter, Path, Query, Cookie, Header
from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date

app03 = APIRouter()

"""路径参数和数字验证"""

@app03.get("/path/parameters")
async def path_params01():
    return {"message": "This is a message"}

@app03.get("/path/{parameters}")
async def path_params01(parameters: str):
    return {"message": parameters}

class CityName(str, Enum): # 定义枚举 使用数据
    Beijing = "Beijing China" 
    Shanghai = "Shanghai China"

@app03.get("/enum/{city}")
async def latest(city: CityName):
    if city == CityName.Shanghai:
        return {"city_name":city, "confirmed": 1492, "death":7}
    if city == CityName.Beijing:
        return {"city_name":city, "confirmed": 971, "death":1}
    return {"city_name":city, "latest":"unknow"}

@app03.get("/files/{file_path:path}") # 通过:path 来传递文件路径
async def filepath(file_path: str):
    return f"This file path is {file_path}"

@app03.get("/path/{num}")
async def path_params_validate(
    num: int = Path(..., title="Num title", description="数字标题", ge=1, le = 10)
):
    return num


"""查询参数和字符串验证"""
@app03.get("/query")
async def page_limit(page: int = 1, limit: Optional[int] = None):
    if limit:
        return {"page": page, "limit": limit}
    return {"page": page}


@app03.get("/query/bool/coversion")
async def type_conversion(param: bool = False):
    return param

@app03.get("/query/validations")
async def query_params_validate(
    value: str = Query(..., min_length=8, max_length=16, regex="^a"),
    values: List[str] = Query(default=["v1","v2"], alias = "别名我是")
): # 多个查询参数的列表，参数别名
    return value, values


"""请求体和字段"""
class CityInfo(BaseModel):
    name: str = Field(..., example="Beijing") # Example 是注解的作用，不会做任何校验
    country: str 
    country_code: str = None
    country_population: int = Field(..., title="Population",description="国家")

    class Config:
        schema_extra = {
            "example" : {
                "name": "Shanghai",
                "country":"China",
                "country_code":"CN",
                "country_population": 140000000
            }
        }
@app03.post("/request_body/city")
async def city_info(city: CityInfo):
    return city.dict()


"""多参数混合"""
@app03.put("/request_body/city/{name}")
async def mix_city_info(
    name: str,
    city01: CityInfo,
    city02: CityInfo,
    confirmed: int = Query(..., ge= 0 , description="确诊数"),
    death: int = Query(..., ge= 0 , description="死亡数")
):
    if name == "Shanghai":
        return {"Shanghai": {"confirmed":confirmed, "death":death}}
    return city01.dict(), city02.dict()

"""数据格式嵌套的请求体"""

class Data(BaseModel):
    city: List[CityInfo] = None
    date: date 
    confirmed: int = Query(..., ge= 0 , description="确诊数")
    death: int = Query(..., ge= 0 , description="死亡数")

@app03.put("/request_body/nested")
async def nested_models(data: Data):
    return data

"""Cookie 和 Header"""
@app03.get("/cookie/")
async def cookie(cookie_id: Optional[str] = Cookie(None)):
    return {"cookie_id": cookie_id}  

@app03.get("/header/")
async def header(user_agent: Optional[str] = Header(None, conver_underscore=True), x_token: List[str] = Header(None)):
    return {"user_agent": user_agent, "x_token": x_token}\

"""BaseModel 参数的使用"""

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
 
@app03.post("/model/")
async def get_base_model(item: Item):
    return  item


