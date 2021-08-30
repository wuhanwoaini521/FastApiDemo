from time import sleep
import json
import unittest
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd
import xlsxwriter as xw
import os


class Config:

    @staticmethod
    def sava_to_excel(self, fileName, data):
        data = list(data)
        job_name = []
        address = []
        pay = []
        edu = []
        hrname = []
        company = []
        company_size = []
        skills = []
        welfare = []
        for i in range(len(data)):
            for j in range(len(data[i])):
                job_name.append(data[i][j]["job_name"])
                print("job_name %s " % job_name)
                address.append(data[i][j]["address"])
                pay.append(data[i][j]["pay"])
                edu.append(data[i][j]["edu"])
                hrname.append(data[i][j]["hrname"])
                company.append(data[i][j]["company"])
                company_size.append(data[i][j]["company_size"])
                skills.append(data[i][j]["skills"])
                welfare.append(data[i][j]["welfare"])

        dfData = {
            '職位名稱': job_name,
            '工作地址': address,
            '薪資範圍': pay,
            '教育程度': edu,
            'HR名字': hrname,
            '公司名稱': company,
            '公司規模': company_size,
            '所需技能': skills,
            '福利待遇': welfare,
        }
        if os.path.exists(fileName):
            print("文件已存在，追加數據開始！")
            df = pd.read_excel(fileName)
            print(df)
            ds = pd.DataFrame(df)
            df = df.append(ds, ignore_index=True)
            df.to_excel(fileName, index=False)
            print("文件已存在，追加數據結束！")
        else:
            print("文件不存在，創建文件！")
            df = pd.DataFrame(dfData)  # 创建DataFrame
            df.to_excel(fileName, sheet_name='職位搜索表', index=False)
            print("文件存入結束，保存成功！")

    @staticmethod
    def save_excel(self, fileName, data):
        workbook = xw.Workbook(fileName)  # 创建工作簿
        worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
        worksheet1.activate()  # 激活表
        title = ['職位名稱', '工作地址', '薪資範圍', '教育程度',
                 'HR名字', '公司名稱', '公司規模', '所需技能', '福利待遇']  # 设置表头
        worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
        i = 2  # 从第二行开始写入数据
        for j in range(len(data)):
            insertData = [data[j]["job_name"], data[j]["address"], data[j]["pay"], data[j]["edu"]
                , data[j]["hrname"], data[j]["company"], data[j]["company_size"], data[j]["skills"], data[j]["welfare"]]
            row = 'A' + str(i)
            worksheet1.write_row(row, insertData)
            i += 1
        workbook.close()  # 关闭表

    @staticmethod
    def get_cookie(self, filePath, driver):
        print("开始获取Cookie，等待20s --> ")
        sleep(20)
        # get cookies
        with open(filePath, 'w') as cookief:
            cookief.write(json.dumps(driver.get_cookies()))
        print("获取 Cookie 结束！并写入文件 %s " % filePath)

    @staticmethod
    def add_cookie(self, driver, filepath):
        driver.delete_all_cookies()
        with open(filepath, 'r') as cookief:
            cookieslist = json.load(cookief)

            for cookie in cookieslist:
                if isinstance(cookie.get('expiry'), float):
                    cookie['expiry'] = int(cookie['expiry'])
                driver.add_cookie(cookie)
        driver.refresh()
