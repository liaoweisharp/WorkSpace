# coding=UTF-8

import requests
params={'$total':1000,'$reload':0,'$pg':1,'$pgsz':1000}
r= requests.post("http://jzsc.mohurd.gov.cn/dataservice/query/comp/regStaffList/001607220057220531", data=params)
print r.text