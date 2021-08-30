from selenium import webdriver

from time import sleep
import json
import unittest
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd
import xlsxwriter as xw
import os

class Base:

    def __init__(self,driver):
        self.driver = driver
        self.job_lists_l = []
        self.j_lists = []

    def search_job(self):
        self.driver.find_element_by_xpath("//li/a[text()='职位']").click()
        # postion
        # "//dl[@class='condition-district  show-condition-district ']/dd/a[text()='甘井子区']"
        # self.driver.find_element_by_xpath("//dl[@class='condition-district  show-condition-district ']/dd/a[text()='甘井子区']").click()
        self.driver.find_element_by_class_name("ipt-search").send_keys("测试工程师")
        self.driver.find_element_by_xpath("//button[@class='btn btn-search']").click()
        # 学历要求
        # ip = //input[@class='ipt' and @value='学历要求']
        ipt = self.driver.find_element_by_xpath("//input[@class='ipt' and @value='学历要求']")

        # 本科
        # bk = //a[text()='本科']
        bk = self.driver.find_element_by_xpath("//a[text()='本科']")
        actions = ActionChains(self.driver)
        actions.drag_and_drop(ipt, bk)
        actions.perform()
        bk.click()
        sleep(5)

    def get_job(self, key_text=None):
        # 存储职位
        j_list = []
        t_dic = {}
        # 职位列表
        job_list = self.driver.find_elements_by_xpath("//div[@class='job-list']/ul/li")
        print("一页共获取到 %d 条数据" % len(job_list))
        for i, job in enumerate(job_list):
            if key_text in job.find_element_by_class_name("tags").text:
                jobs_list = job.text.split("\n")
                flag = True
                while flag:
                    if len(jobs_list) < 9:
                        jobs_list.append("")
                        flag = True
                    else:
                        flag = False
                # 職位信息添加到字典中
                t_dic = {}
                t_dic["job_name"] = jobs_list[0]
                t_dic["address"] = jobs_list[1]
                t_dic["pay"] = jobs_list[2]
                t_dic["edu"] = jobs_list[3]
                t_dic["hrname"] = jobs_list[4]
                t_dic["company"] = jobs_list[5]
                t_dic["company_size"] = jobs_list[6]
                t_dic["skills"] = jobs_list[7]
                t_dic["welfare"] = jobs_list[8] # 出现了有公司没有这个字段的情况
                j_list.append(t_dic)
                # j_list.append(job.text.split("\n"))
        print("根据关键字 %s 搜索出的有效数据， 共計： %d 條。" % (key_text, len(j_list)))

        self.j_lists.append(j_list)
        print("j_lists -> %s " % self.j_lists)
        return j_list

    def turnPage(self, key_text):
        """进行页面翻页操作"""
        # 翻页按钮
        flag = True
        while flag:
            next_btn = self.driver.find_element_by_class_name("next")
            if "disable" in next_btn.get_attribute("class"):
                print("最后一页了！")
                flag = False
            else:
                # 先获取当前页面的数据，再点击下一页
                self.current_page()

                j_list =self.get_job(key_text)
                self.job_lists_l.append(j_list)
                next_btn.click()
                flag = True
                print("job_lists_l -> %s  " % self.job_lists_l)
        return self.job_lists_l

    def current_page(self):
        # 查看当前是第几页
        page_num = self.driver.find_elements_by_xpath("//div[@class='page']/a")
        for ele in page_num:
            if "cur" in ele.get_attribute("class"):
                page_num = ele.text
        print("当前是第 %s 页" % page_num)
        return page_num


    def count_page(self):
        """统计现在读取了多少页"""
        pass