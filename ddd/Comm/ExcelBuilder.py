# coding=UTF-8
import random
import traceback

import datetime
import xlrd
import sys   #解决乱码问题
reload(sys)   #解决乱码问题

class ExcelBuilder:
    def __init__(self,path):
        self.path=path
        self.header=[] #表头
    def readSheet(self,index,fromX=0,fromY=0,returnType="元组"):
        '''
        读取第n个sheet(n从0开始)
        :param index: sheet编号（从0开始）
        :param fromX: 从第x行开始读取（从0开始）
        :param fromY: 从第y列开始读取（从0开始）
        :return: 返回元组/json的列表
        '''
        result=[]
        try:
            data = xlrd.open_workbook(self.path)
            table = data.sheets()[index]
            if fromX<table.nrows and fromY<table.ncols :
                for x in range(fromX,table.nrows):

                    if returnType=="元组":
                        row=()
                    else:
                        row = {}
                    num=0
                    for y in range(fromY,table.ncols):
                        value=table.cell(x, y).value      #获取单元格的值
                        value = self.vaildNumber(value)
                        row[num] = value
                        if x==fromX:
                            self.header.append(num)       #添加到表头的列表中
                        num+=1
                    result.append(row)
        except:
            traceback.print_exc()
            result= None
        finally:
            self.data=result
            return result
    def getData(self):
        '''
        得到数据
        :return: json/元组  列表
        '''
        return self.data
    def getHeader(self):
        return self.header
    def delByIndex(self,index):
        '''
        删除索引列
        :param index: 索引号
        :return: 
        '''
        self.header.pop(index)
    def insertByIndex(self,index, value,colName=None):
        '''
        插入索引列
        :param index: 插入的索引位置
        :param value: 插入的值
        :param colName: 列名（可选）
        :return: 
        '''
        if colName is None:
            colName = self.getRandomNum()
        self.header.insert(index, colName)
        for row in self.data:
            row[colName] = value
    def selectIndexs(self,indexList):
        '''
        获得索引列的值
        :param indexList: 
        :return: 
        '''
        newHeader=[]
        for index in indexList:
            #这里要处理越界的异常
            newHeader.append(self.header[index])
        self.header=newHeader
    def getRandomNum(self):
        '''
        生成随机数
        :return: 
        '''
        nowTime = datetime.datetime.now().strftime("%Y%m%d%H%M%S");  # 生成当前时间
        randomNum = random.randint(0, 100);  # 生成的随机整数n，其中0<=n<=100
        if randomNum <= 10:
            randomNum = str(0) + str(randomNum);
        uniqueNum = str(nowTime) + str(randomNum);
        return uniqueNum;
    def vaildNumber(self,value):
        '''
        去掉整数后面的.0(如： 12345678.0 -》 12345678)
        :param value: 
        :return: 
        '''
        result=value
        try:
            _value=float(value)
            if(int(_value)==value):
                result=int(_value)
        finally:
            return result
