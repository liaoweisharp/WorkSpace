
# coding=UTF-8
import sys
from selenium import webdriver
import time
reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题

driver=webdriver.PhantomJS(executable_path=r"D:\Python27\phantomjs-2.1.1-windows\bin\phantomjs.exe")
driver.get("http://passport.cnblogs.com/login.aspx?ReturnUrl=http://www.cnblogs.com/fnng/admin/EditPosts.aspx")

time.sleep(3)
driver.maximize_window() # 浏览器全屏显示

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