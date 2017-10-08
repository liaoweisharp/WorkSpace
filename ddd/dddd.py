# coding=UTF-8
import sys
import datetime
import os

import cc.class1
import DataBase.DatabaseDAL


def main():
    pass



    list=[{"co_XinYongCode":"value1","co_QiYeMingCheng":"value2","co_FaRen":"value3","co_ZhuCeDi":"四川","co_Href":"ssss"},
          {"co_XinYongCode": "value1", "co_QiYeMingCheng": "value2", "co_FaRen": "张学友", "co_ZhuCeDi": "四川", "co_Href": "ssss"}]

    obj=DataBase.DatabaseDAL.DatabaseDAL()
    n=obj.insert("Tab_ZJB_Company",list)

    try:
        aaa=1/10
    except:
        print "except"
        aaa=None
    else:
        print "a={0}".format(aaa)
    finally:
        if aaa is not None:
            print "finally={0}".format(aaa)
        else:
            print "finally=None"
    # '''
    # dd=os.stat('dddd.py')
    # print type(dd)
    # print dd.st_size
    # print datetime.datetime.fromtimestamp(dd.st_atime)
    # print datetime.datetime.fromtimestamp(dd.st_ctime)
    # print "当前路径：",os.getcwd()
    # print "当前路径的文件："
    # print os.listdir(os.getcwd())
    # for dir in sys.path:
    #     print dir
    # print "*" * 20
    # obj= cc.class1.class1(30,"前期")
    # print type(obj)
    # print obj.name
    # print "*" * 20
    #
    # help(obj)


def fun1(name , **args):
    print "name={0}".format(name)
    print "args={0}".format(args)
def fun2(name , *args):
    print "name={0}".format(name)
    print "args={0}".format(args)

print "dddddd=",__name__
if __name__=="__main__":
    main()

