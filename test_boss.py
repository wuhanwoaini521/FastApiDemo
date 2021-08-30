# -*- coding:utf-8 -*-
from selenium import webdriver

from time import sleep
import json
import unittest
import os
from selenium.webdriver.common.action_chains import ActionChains

from base import Base
from config import Config

class Test_boss(unittest.TestCase):

    def setUp(self) -> None:
        # 读取用户本地缓存
        option = webdriver.ChromeOptions()
        option.add_argument(r"user-data-dir=C:\Users\EDZ\AppData\Local\Google\Chrome\User Data")  # 浏览器路径
        # 初始化driver
        self.driver = webdriver.Chrome(options=option)

        # self.driver = webdriver.Chrome()
        self.driver.get("https://www.zhipin.com/web/geek/recommend")
        sleep(3)
        self.driver.maximize_window()
        self.driver.implicitly_wait(10)

        sleep(3)

        self.b = Base(driver=self.driver)
        self.c = Config()



    def test_search(self):
        self.b.search_job()
        data = self.b.turnPage("SQL")
        print("data -> %s" % data)
        # 存入 excel
        fileName = os.path.dirname(os.path.abspath(__file__)) + "/boss.xlsx"
        self.c.sava_to_excel(self, data=data, fileName=fileName)

    def tearDown(self) -> None:
        sleep(3)
        self.driver.close()

if __name__ == '__main__':
    unittest.main()


