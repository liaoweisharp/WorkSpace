# coding=UTF-8
import traceback

import requests

url = "http://www.zzcx365.com/WebService/WebService_ExportExcel.asmx/getFilter"
data ={"pc":{"currentPageNumber":0,"pageSize":20},"companyId":"","userName":"","zhengShuArr":[]}

try:
    page = requests.post(url, json=data,headers={"Content-Type": "application/json"})
    print page.text
except :
    traceback.print_exc()
