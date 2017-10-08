import re
from urllib import urlopen
from bs4 import BeautifulSoup

try:
    aa=[]
    bb=set()

    html=urlopen("http://www.pythonscraping.com/pages/page3.html")
    bsObj=BeautifulSoup(html,"html.parser")
    p=bsObj.find(name="table",attrs={"id":"giftList"})
    imgs=p.findAll(name="img",attrs={"src":re.compile("\.\.\/img\/gifts\/img.*\.jpg")})
    for img in imgs:
        print img.attrs["src"]

    # for tr in p.descendants:
    #     print "*"* 20
    #     print tr
    # print type(p.children)
    # print "children len={0}".format(len(p.children))
    # print "descendants len={0}".format(len(p.descendants))
        # nameList=bsObj.findAll("span",{"class":"green"})
    # nameList2 = bsObj.findAll("span", {"class": "red"})
    #
    # nameList3 = bsObj.findAll("span", {"class": ["red","green"]})
    # nameList4 = bsObj.findAll(name=["h1","h2"])
    # nameList5 = bsObj.findAll(name={"h1", "h2"})
    # for name in nameList:
    #     print name.get_text()
except:
    print "Exception:"
else:
    print "else"
#

