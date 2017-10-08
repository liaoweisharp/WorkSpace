# coding=UTF-8
import requests

session=requests.session()

par={'username':'abc','password':'password'}
r=requests.post("http://pythonscraping.com/pages/cookies/welcome.php",par)
cookies=r.cookies
print r.cookies.get_dict()
print r.text
print "传cookies的情况："
r=requests.get("http://pythonscraping.com/pages/cookies/welcome.php",cookies=cookies)
print r.cookies.get_dict()
print r.text
print "不传cookies的情况："
r=requests.get("http://pythonscraping.com/pages/cookies/welcome.php")
print r.cookies.get_dict()
print r.text
