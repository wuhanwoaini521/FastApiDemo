# -*- coding:utf-8 -*-
import unittest

# @Screen
# class ClassA(unittest.TestCase):
#     driver = None  # driver是一个WebDriver实例
#
#     @classmethod
#     def setUpClass(cls):
#         cls.driver = webdriver.Chrome()
#
#     def tearDown(self):
#         self.driver.close()
#         self.driver.quit()
#
#     def test_001(self):
#         self.driver.get("http://www.baidu.com")
#         raise AttributeError
#
#
#     # example_2:
# class ClassB(unittest.TestCase):
#     driver = None  # driver是一个WebDriver实例
#
#     @classmethod
#     def setUpClass(cls):
#         cls.driver = webdriver.Chrome()
#
#     def tearDown(self):
#         self.driver.close()
#         self.driver.quit()
#
#     @Screen
#     def test_001(self):
#         self.driver.get("http://www.baidu.com")
#         raise AttributeError
#
from selenium import webdriver

from demo.screen import web_screen


@web_screen
class ClassA(unittest.TestCase):
    # driver = webdriver.Chrome()  # driver是一个WebDriver实例

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()

    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        cls.driver.quit()

    @web_screen(msg="预期标记失败", type=True)
    @unittest.expectedFailure
    def test_001(self):
        self.driver.get("http://www.baidu.com")
        # raise AttributeError("--主动异常--")
        self.driver.find_element_by_xpath("sss")
