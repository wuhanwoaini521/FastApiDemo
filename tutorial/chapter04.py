
from fastapi import APIRouter
from typing import List, Optional
from pydantic import BaseModel,EmailStr
"""
    响应
"""

app04 = APIRouter()

class Base_User(BaseModel):
    username: str
    # password: str
    email: EmailStr
    mobile: str = "10086"
    address: Optional[str] = None
    full_name: Optional[str] = None

class UserIn(Base_User):
    password: str

class UserOut(Base_User):
    pass

@app04.post('/', response_model=UserOut, response_model_exclude_unset=True)
async def response_model(user: UserIn):
    return user