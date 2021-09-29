'''
Author: han wu 
Date: 2021-08-30 21:43:21
LastEditTime: 2021-09-26 22:27:15
LastEditors: your name
Description: 
FilePath: /FastApiDemo/tutorial/chapter06.py
~~~~~~~~~吼吼吼~~~~~~~~~~
'''

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

app06 = APIRouter()

oauth_schema = OAuth2PasswordBearer("/chapter06/token") # 通过请求这个路径来获取token
@app06.get("/oauth2_password_bearer")
async def oauth2_password_bearer(token: str = Depends(oauth_schema)):
    return {"token": token}

# 模拟一下数据库
fake_user_db = {
	"john snow":{
		"username": "john snow",
		"full_name": "John Snow",
		"email": "johnsnow@example.com",
		"hashed_password": "fakehashedsecret",
		"disable": False,
	},
	"alice":{
		"username": "alice",
		"full_name": "Alice",
		"email": "alice@example.com",
		"hashed_password": "fakehashedsecret2",
		"disable": True
	}
}
