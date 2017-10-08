# coding=UTF-8
##******************************************************************************
## **  文件名称: readExcel3.py
## **  功能描述: excel文件入库hive表（集团标签）
## **  入库表：MUSIC_DESCRIPTIVE_DESC_TEMP
## **
## **
## **  创建者:   Liao Wei
## **  创建日期: 20170728
## **  修改日志:
## **  修改日期:
# ** ---------------------------------------------------------------
# **
# ** ---------------------------------------------------------------
# **
# **  程序调用格式：python readExcel3.py excel文件绝对路径 生成txt绝对路径 20170728
# **
#*******************************************************************************


import os
import sys
import traceback

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append("..")
import Comm.ExcelBuilder
import Comm.DateBuilder

if len(sys.argv) != 4:
    print  '参数错误! 应该是3个参数'
    sys.exit(0)
path = sys.argv[1]
newPath=sys.argv[2]
_dealday=sys.argv[3]
# path = 'C:\\3.xlsx'
# newPath='D:\\3.txt'
# _dealday='20170728'
targetTable='MUSIC_DESCRIPTIVE_DESC_TEMP' ## 入库表
splitCol='\t'
splitRow='\n'
dayWeek=4 ## 星期4 处理
data = []
headers = None

def main():
    global data, headers
    dealday=getDealDay(_dealday)
    excelBuilder = Comm.ExcelBuilder.ExcelBuilder(path)
    data=excelBuilder.readSheet(0,fromX=1,fromY=0,returnType="字典")
    if data is not None:
        excelBuilder.selectIndexs([0, 1, 2, 3, 5, 6, 7, 4])
        excelBuilder.insertByIndex(8,dealday)
    headers=excelBuilder.getHeader()
    data = excelBuilder.getData()
    ## 逗号替换成竖线 （情感、主题、风格、对象、场景）
    doReplace(data,headers)
    exportFile(newPath)
    os.system('sh insertHive.sh {0} {1}'.format(newPath,targetTable))

def doReplace(data,headers):
    indexList=[3,4,5,6,7]
    for row in data:
        for index in indexList:
            cellData=row[headers[index]]
            if cellData is not None:
                row[headers[index]] = cellData.replace(",","|")
                row[headers[index]] = row[headers[index]].replace("，", "|")

def getDealDay(_dealday):
    dateBuilder = Comm.DateBuilder.DateBuilder()
    week = dateBuilder.getweekmsg(_dealday)  # 第几周
    dayList = dateBuilder.getWeekDays('{0}{1}'.format(week[0], week[1]))  # 周的起始时间
    return dayList[dayWeek - 1]

def exportFile(filePath):
    '''
    导出文件
    :param filePath: 
    :return: 
    '''
    lines = []
    global data,headers
    for row in data:
        cols=[]
        for header in headers:
            cols.append(row[header])
        rowStr=splitCol.join(map(str,cols))
        rowStr +=splitRow
        lines.append(rowStr)

    try:
        file=open(filePath,'w')
        file.writelines(lines)
    except:
        traceback.print_exc()
    finally:
        file.close()
    pass
# def 入库:
#     pass
if __name__=="__main__":

    main()