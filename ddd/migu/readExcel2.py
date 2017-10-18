# coding=UTF-8
##******************************************************************************
## **  文件名称: readExcel2.py
## **  功能描述: excel文件入库hive表（营销用语）
## **  入库表：vgop_dim_picture_sale
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
# **  程序调用格式：python readExcel2.py excel文件绝对路径 生成txt绝对路径 20170728
# **
#*******************************************************************************
#
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
# path = 'C:\\2.xlsx'
# newPath='D:\\2.txt'
# _dealday='20170728'
targetTable='vgop_dim_picture_sale' ## 入库表
splitCol='\t'
splitRow='\n'
dayWeek=4 ## 星期4 处理
data = []
headers = None

def main():
    try:
        global data, headers
        dealday=getDealDay(_dealday)

        excelBuilder = Comm.ExcelBuilder.ExcelBuilder(path)
        _data=excelBuilder.readSheet(0,fromX=1,fromY=0,returnType="字典")
        if _data is not None:
            excelBuilder.insertByIndex(0, dealday,'col'+dealday)
            data.extend(excelBuilder.getData())
        _data = excelBuilder.readSheet(1, fromX=1, fromY=0, returnType="字典")
        if _data is not None:
            excelBuilder.insertByIndex(0, dealday,'col'+dealday)
            data.extend(excelBuilder.getData())
        excelBuilder.selectIndexs([0,7,18,20])

        headers=excelBuilder.getHeader()
        exportFile(newPath)
        os.system('sh insertHive.sh {0} {1} > /dev/null 2>&1'.format(newPath, targetTable))
    except:
        traceback.print_exc()
    else:
        print "0"

def getDealDay(_dealday):
    '''
    得到处理日
    :param _dealday: 
    :return: 
    '''
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