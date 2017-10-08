
# coding=UTF-8
import sys
from selenium import webdriver
import time
reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题

driver = webdriver.Firefox(executable_path="D:\Python27\WorkSpace\ddd\geckodriver.exe")
driver.get("http://www.dianhua.cn/shijiazhuang/c160/p2")

time.sleep(3)
driver.get_screenshot_as_file("c://a.png") # 浏览器全屏显示

#通过用户名密码登陆
driver.find_element_by_id("input1").send_keys("Liao Wei")
driver.find_element_by_id("input2").send_keys("liaowei")

#勾选保存密码
driver.find_element_by_id("remember_me").click()
time.sleep(3)
#点击登陆按钮
driver.find_element_by_id("signin").click()

#获取cookie信息并打印
cookie= driver.get_cookies()
print cookie
print "*" * 20
time.sleep(2)
print driver.page_source

driver.close()