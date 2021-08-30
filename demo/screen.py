#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Date  : 2020/12/18
# @Author  : See You_HQ
# @Email   : h513654786@outlook.com
# @File    : screen.py
# @Software: PyCharm
"""
# coding=utf-8
import re
import traceback

"""
用例执行失败自动截图，适用于test_
"""
import os
import sys


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# moudle_path = os.path.join(os.path.dirname(BASE_DIR))
# sys.path.append(moudle_path)
# cur_path = os.path.dirname(os.path.realpath(__file__))
# Report_path = os.path.join(os.path.dirname(cur_path), "Report")

import functools
import inspect

screen_path_bug = os.path.join(os.path.dirname("."), 'Report\\Screen\\bug\\')
screen_path_true = os.path.join(os.path.dirname("."), 'Report\\Screen\\')
# 默认创建的报错截图文件路径Report\\Screen\\
Report = screen_path_bug
if os.path.isdir(Report):
    pass
else:
    os.makedirs(Report)


# print(png_path)

# web端自定义截图方法
def screen_save(driver, msg="null", type=False):
    if type is False:
        png_name = screen_path_bug + "False" + str(msg) + ".png"
    else:
        png_name = screen_path_true + "True" + str(msg) + ".png"
    img_base64 = driver.get_screenshot_as_base64()
    driver.save_screenshot(png_name)  # args[0].driver对应测试类中的driver

    # print(f"base64_[{png_name}]_save:{img_base64}")  # args[0].driver对应测试类中的driver
    # screen={}
    # print("args", list(args))
    # print("args_type", type(args))

# web端出现错误自动截图防范
def web_screen(target=None, func_prefix="test", msg="null", type=False):
    """
    默认截图为错误。出现异常自动截图，msg为保存的附加信息，截图保存路径./Screen/bug；type不为Falses，时，截图保存路径为./Screen
    """
    def decorator(func_or_cls):
        if inspect.isfunction(func_or_cls):
            @functools.wraps(func_or_cls)
            def web_aberrant_snapshot(*args, **kwargs):
                try:
                    return func_or_cls(*args, **kwargs)
                except Exception as e:  # 可以修改要捕获的异常类型
                    # e_line=str(args[0].tb_lineno)
                    # 返回调用函数截图报错所在行，加入截图命名中
                    err_back_line = re.search(r'line.[0-9]*', (traceback.format_exc(limit=-1))).group()
                    if type is False:
                        png_name = screen_path_bug + str(args[0]) + str(err_back_line) + str(msg) + ".png"

                    else:
                        png_name = screen_path_true + "主动异常截图" + str(args[0]) + str(err_back_line) + str(msg) + ".png"

                    img_base64 = str(args[0].driver.get_screenshot_as_base64())
                    args[0].driver.save_screenshot(png_name)  # args[0].driver对应测试类中的driver
                    print(f"web自动异常截图_[msg={msg}]_save:{png_name}")  # args[0].driver对应测试类中的driver

                    # print(f"自动错误截图base64_[{png_name}]_save:{img_base64}")  # args[0].driver对应测试类中的driver
                    # 返回调用函数截图报错所在行
                    # err_traceback_line = re.search(r'line.[0-9]*', (traceback.format_exc(limit=-1))).group()
                    # print("func_or_cls==>", str(err_traceback_line))
                    # print("func_or_cls  last==>", traceback.print_last)
                    # print("args_type", dir(args))
                    # if type is False:
                    #     log.error(png_name)
                    # else:
                    #     log.info(png_name)
                    raise

            return web_aberrant_snapshot
        elif inspect.isclass(func_or_cls):
            for name, func in list(func_or_cls.__dict__.items()):
                if inspect.isfunction(func) and name.startswith(func_prefix):
                    setattr(func_or_cls, name, decorator(func))
            return func_or_cls
        else:
            # print("target_before", target)
            raise AttributeError

    if target:
        return decorator(target)
    else:
        return decorator


def app_screen(target=None, func_prefix="test", msg="null", type=False):
    """
    默认截图为错误。出现异常自动截图，msg为保存的附加信息，截图保存路径./Screen/bug；type不为Falses，时，截图保存路径为./Screen
    """
    def decorator(func_or_cls):
        if inspect.isfunction(func_or_cls):
            @functools.wraps(func_or_cls)
            def app_aberrant_snapshot(*args, **kwargs):
                try:
                    return func_or_cls(*args, **kwargs)
                except Exception as e:  # 可以修改要捕获的异常类型
                    err_back_line = re.search(r'line.[0-9]*', (traceback.format_exc(limit=-1))).group()
                    if type is False:
                        png_name = screen_path_bug + str(args[0]) + str(err_back_line) + str(msg) + ".png"
                    else:
                        png_name = screen_path_true + "主动异常截图" + str(args[0]) + str(err_back_line) + str(msg) + ".png"


                    print(f"app自动异常截图_[msg={msg}]_save:{png_name}")  # args[0].driver对应测试类中的driver
                    raise

            return app_aberrant_snapshot
        elif inspect.isclass(func_or_cls):
            for name, func in list(func_or_cls.__dict__.items()):
                if inspect.isfunction(func) and name.startswith(func_prefix):
                    setattr(func_or_cls, name, decorator(func))
            return func_or_cls
        else:
            # print("target_before", target)
            raise AttributeError

    if target:
        return decorator(target)
    else:
        return decorator


class Screen(object):
    """
    类装饰器, 功能与screen一样
    """

    def __new__(cls, func_or_cls=None, func_prefix="test"):
        cls._prefix = func_prefix
        self = object.__new__(cls)
        if func_or_cls:
            return self(func_or_cls)
        else:
            return self

    def __init__(self, target=None, func_prefix="test"):
        # self.target = "None"
        pass

    def __call__(self, func_or_cls=None):

        if inspect.isfunction(func_or_cls):
            @functools.wraps(func_or_cls)
            def wrapper(*args, **kwargs):
                try:
                    return func_or_cls(*args, **kwargs)
                except Exception:  # 可以修改要捕获的异常类型

                    png_name = screen_path_bug + str(args[0]) + ".png"
                    args[0].driver.save_screenshot(png_name)  # args[0].driver对应测试类中的driver
                    # print("args", list(args))
                    # print("args_type", type(args))
                    # print(kwargs)

                    raise

            return wrapper
        elif inspect.isclass(func_or_cls):
            for name, func in list(func_or_cls.__dict__.items()):
                if inspect.isfunction(func) and name.startswith(self._prefix):
                    setattr(func_or_cls, name, self(func))
            return func_or_cls
        else:
            raise AttributeError

if __name__ == '__main__':
    import unittest
    import selenium.webdriver as webdriver


    @Screen
    class ClassA(unittest.TestCase):
        driver = None  # driver是一个WebDriver实例

        @classmethod
        def setUpClass(cls):
            cls.driver = webdriver.Chrome()

        def tearDown(self):
            self.driver.close()
            self.driver.quit()

        def test_001(self):
            self.driver.get("http://www.baidu.com")
            raise AttributeError


    # example_2:
    class ClassB(unittest.TestCase):
        driver = None  # driver是一个WebDriver实例

        @classmethod
        def setUpClass(cls):
            cls.driver = webdriver.Chrome()

        def tearDown(self):
            self.driver.close()
            self.driver.quit()

        @Screen
        def test_001(self):
            self.driver.get("http://www.baidu.com")
            raise AttributeError
#
