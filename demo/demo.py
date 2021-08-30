import time
from functools import wraps

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import traceback


# 元素高亮
def highlight(func):
    def apply_style(element):
        js = "arguments[0].style.border='2px solid red'"
        # 实现的方式很简单，就是定位到元素后，执行js样式
        driver.execute_script(js, element)

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        element = func(self, *args, **kwargs)
        print("element: %s " % element)
        apply_style(element)
        return element

    return wrapper


# 截图（完整截图）
def screenshot(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        element = func(self, *args, **kwargs)  # func 传入得是一个 webElement 对象
        if not element:
            element = driver.save_screenshot(args[-1] + '.png')  # 默认是以定位元素属性为文件名
            print("异常截图")
        return element

    return wrapper


class Action(object):
    def __init__(self, driver):
        self.driver = driver

    @screenshot
    # @highlight
    def find_element(self, *loc):
        try:
            WebDriverWait(self.driver, 3).until(lambda driver: driver.find_element(*loc).is_displayed())
            return self.driver.find_element(*loc)
        except Exception as e:
            # driver.save_screenshot(loc[-1] + '.png')
            print("traceback.format_exc %s " % traceback.format_exc(1))
            return False


driver = webdriver.Chrome()

driver.get('http://www.baidu.com')

action = Action(driver)
action.find_element(By.ID, 'kw1k')
action.find_element(By.ID, 'su')

time.sleep(3)
driver.quit()
