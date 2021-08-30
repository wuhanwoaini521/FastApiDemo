from datetime import datetime, date
from typing import List, Optional
from pathlib import Path
from pydantic import BaseModel,ValidationError, constr  # 限制字符串长度
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base

class User(BaseModel):
    id: str
    name: str = "Wuhan"
    signup_ts: Optional[datetime] = None
    friends: List[int] = []  # 如果传入的数据是非int类型但是，可以转换成int类型的数据也是可以的->"1"


external_data = {
    "id": "123",
    "signup_ts": "2022-12-22 12:22",
    "friends": [1, 2, '3']
}
print("\33[91m1. --------" + " Pydantic 测试" + "-------- \33[0m")
user = User(**external_data)
print(user.id, user.signup_ts, user.friends, user.name)
print(repr(user.signup_ts))
print(user.dict())

print("\33[91m2. --------" + " 校验失败处理 " + "-------- \33[0m")
try:
    User(id='1234', signup_ts=datetime.today(), friends=[1,2,'not number'])
except ValidationError as e:
    print(e.json())  # 发生ValidationError（验证错误）抛出的异常可以按照json格式捕获

print("\33[91m3. --------" + " 模型类的属性和方法 " + "-------- \33[0m")
print(user.dict())
print(type(user.dict()))
print(user.json())
print(type(user.json()))
print(user.copy())
print(type(user.copy()))
print(User.parse_obj(obj=external_data))  # 解析数据
print(User.parse_raw('{"id": "123", "name": "Wuhan", "signup_ts": "2022-12-22T12:22:00", "friends": [1, 2, 3]}'))  # 解析原生key：value形式
# 导入文件，写入文件
path = Path('pydantic_tutorial.json')
path.write_text('{"id": "123", "name": "Wuhan", "signup_ts": "2022-12-22T12:22:00", "friends": [1, 2, 3]}')
print(User.parse_file(path))

print(user.schema())
print(user.schema_json())
user_data = {"id": "error", "name": "Wuhan", "signup_ts": "2022-12-22T12:22:00", "friends": [1, 2, 3]}
print(user.construct(**user_data)) # construct 不校验传入参数的格式，直接创建模型类，这种情况不安全 不建议使用

# 查看字段的输出顺序，和所有字段
print(User.__fields__.keys())

print("\33[91m3. --------" + " 递归模型 " + "-------- \33[0m")


class Sound(BaseModel):
    sound: str # 如果下层需要调用的话，那么就需要传入一个字典，不能单独传一个字符串


class Dog(BaseModel):
    birthday: date
    weight: float = Optional[None]
    sound: List[Sound]

dogs = Dog(birthday= date.today(), weight=6.66, sound=[{"sound":"wangwangwang~ "},{"sound":"wuwuwu~"}])
print(dogs.dict())

print("\33[91m3. --------" + " ORM模型：从类实例创建符合ORM对象的模型 " + "-------- \33[0m")
Base = declarative_base()

# 建表
class CompanyOrm(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True, nullable=False)
    public_key = Column(String(20), index=True, nullable=False,unique=True)
    name = Column(String(63), unique=True)
    domains = Column(ARRAY(String(255)))

class CompanyMode(BaseModel):
    id: int
    public_key: constr(max_length=20)
    name: constr(max_length=63)
    domains: List[constr(max_length=255)]

    class Config:
        orm_mode = True
co_orm = CompanyOrm(
    id= 123,
    public_key= 'foobar',
    name= 'Testing',
    domains=['example.com','imooc.com']
)
print(CompanyMode.from_orm(co_orm))  # 使用from_ormm方法来使orm对象转换称为pydantic对象


