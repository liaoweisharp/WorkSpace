from selenium import webdriver
import time

def main():
    driver=webdriver.PhantomJS(executable_path=r"D:\Python27\phantomjs-2.1.1-windows\bin\phantomjs.exe")
    #driver = webdriver.PhantomJS(executable_path='phantomjs')
    driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
    print driver.find_element_by_id('content').text
    time.sleep(6)
    print "*"*20
    print driver.find_element_by_id('content').text
    driver.close()


if __name__ == "__main__":
    main()

