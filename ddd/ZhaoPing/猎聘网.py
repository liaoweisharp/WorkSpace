# coding=UTF-8
import sys
import traceback

import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import json
import urllib
import random
sys.path.append("..")
import DataBase.DatabaseDAL
# import global_Vars
import Comm.Funs

def main():

    try:
        ##需要改数据库名
        cookiesStr = "abtest=0; _fecdn_=1; gr_user_id=4ec12565-edd9-4b44-9809-a9ee9dbe7bb3; gr_session_id_bad1b2d9162fab1f80dde1897f7a2972=b343cac0-0fe4-400d-aef9-fb827b6d6ab0; __uuid=1499073780008.56; _uuid=07C2A97FFFA8480C0B80949405BDF1A0; user_name=%E5%90%95%E4%B8%BB%E7%AE%A1; lt_auth=7ugMOicFz1Tw5STR2GNWsqoZiN6tWGqa8i8L1xoJ1oW0XPzq4P3iQQKFqLUAxBIhlRkmJMULNbn3%0D%0ANe%2F9wHJM7UIQwGmnloC5o%2F%2Bk1nw5HbVlL%2F31g%2Fytlc6CQ80ily8EzntkrnsSkk%2Fw4UUratHT2WPh%0D%0AjprX172s%0D%0A; UniqueKey=ed1cc128dbe40b4e1a667e00ad0d9493; user_kind=1; _l_o_L_=70c854113a2374dced1cc128dbe40b4e1a667e00ad0d9493; login_temp=islogin; _e_ld_auth_=4ef88ae32ed2e810; em_username=9716323484v2174783662; em_token=YWMttUU9ME88EeeNrRsN1m_saE8TxtBqMxHkgus5YKfC9XFH0c_wdiwR5pE8113ekbjQAwMAAAFcmxnZmQBPGgDAoME5JZCVXPhOvadZJk7cJT69KsaHfNhePX1tew7ylQ; fe_lpt_event616=true; JSESSIONID=C404C57551E943D8D6603F0A989B85A7; __tlog=1499073780010.69%7C00000000%7C00000000%7Cs_00_pz1%7Cs_00_pz1; __session_seq=5; __uv_seq=5; b-beta2-config=%7B%22hasPhoneNum%22%3A%221%22%2C%22ecreate_time%22%3A%2220151221%22%2C%22v%22%3A%222%22%2C%22d%22%3A269%2C%22e%22%3A8638211%2C%22ejm%22%3A%221%22%2C%22entry%22%3A%221%22%2C%22p%22%3A%220%22%2C%22n%22%3A%22%25E5%2590%2595%25E4%25B8%25BB%25E7%25AE%25A1%22%2C%22audit%22%3A%221%22%2C%22ecomp_id%22%3A8638211%2C%22jz%22%3A%220%22%2C%22version%22%3A%222%22%7D; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1499073781; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1499073947; gr_session_id_2abfd0d7eaa44a729d761fb028300b6c=6a658334-0756-4f79-a839-2b034b09e71c; gr_cs1_6a658334-0756-4f79-a839-2b034b09e71c=user_id%3Afc82407bec7b0cdb4d8d6a58c213b7f2; _mscid=s_00_pz1"
        cookiesJson = Comm.Funs.strConvertDic(cookiesStr)
        # url = 'http://ehire.51job.com/Navigate.aspx?ShowTips=11&PwdComplexity=N'
        # r = requests.get(url,cookies=cookiesJson, verify=False, headers={
        #     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"})
        url = "https://lpt.liepin.com/soresume/so/"
        data={}
        data["filterDownload"] = "1"
        data["searchLevel"] = ""
        data["keysRangType"] = ""
        data["keys"] = ""
        data["dqs"] = "280020"
        data["contains_wantdq"] = "1"
        data["industrys"] = ""
        data["jobtitles"] = ""
        data["workyears"] = ""
        data["age"] = ""
        data["sex"] = ""
        data["updateDate"] = ""
        data["yearSalarylow"] = ""
        data["yearSalaryhigh"] = ""
        data["wantYearSalaryLow"] = ""
        data["wantYearSalaryHigh"] = ""
        data["userStatus"] = ""
        data["language_content"] = ""

        r = requests.post(url, data=data, cookies=cookiesJson, verify=False, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
        print r.text
    except:
        traceback.print_exc()

if __name__=="__main__":
    main()