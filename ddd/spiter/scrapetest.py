from urllib import urlopen
from bs4 import BeautifulSoup

try:

    html=urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
    bsObj=BeautifulSoup(html,"html.parser")
    p=bsObj.find("p")
    nameList=bsObj.findAll("span",{"class":"green"})
    nameList2 = bsObj.findAll("span", {"class": "red"})

    nameList3 = bsObj.findAll("span", {"class": ["red","green"]})
    nameList4 = bsObj.findAll(name=["h1","h2"])
    nameList5 = bsObj.findAll(name={"h1", "h2"})
    for name in nameList:
        print name.get_text()
except:
    print "Exception:"
else:
    print "else"
#

