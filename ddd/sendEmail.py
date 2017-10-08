# coding=UTF-8

import smtplib
import time

message = """From: neirongbianji <neirongbianji@12530.com> 
To: liaowei <liaowei@si-tech.com.cn> 
Subject: ceshi 

这是一封测试邮件。 
"""



def main():
    pass
    time.sleep(10)
    s=smtplib.SMTP()
    try:
        s.connect("221.176.9.235", "25")
    except:
        print "网络不通！"
    state = s.login("neirongbianji@12530.com", "MGYY#2016%")
    s.sendmail("neirongbianji@12530.com",["liaowei@si-tech.com.cn"],message)
    s.quit()

if __name__=="__main__":
    main()