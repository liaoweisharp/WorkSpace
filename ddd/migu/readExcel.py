# coding=UTF-8
##******************************************************************************
## **  文件名称: readExcel.py
## **  功能描述: excel文件入库hive表（咪咕音乐榜）
## **  入库表：VGOP_MUSIC_CHARTS_MGM
## **
## **
## **  创建者:   Liao
## **  创建日期: 20170728
## **  修改日志:
## **  修改日期:
# ** ---------------------------------------------------------------
# **
# ** ---------------------------------------------------------------
# **
# **  程序调用格式：python readExcel.py excel文件绝对路径 生成txt绝对路径 20170728
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

# if len(sys.argv) != 4:
#     print  '参数错误! 应该是3个参数'
#     sys.exit(0)
# path = sys.argv[1]
# newPath=sys.argv[2]
# _dealday=sys.argv[3]
path = 'C:\\1.xlsx'
newPath='D:\\1.txt'
_dealday='20170728'
targetTable='VGOP_MUSIC_CHARTS_MGM' ## 入库表
splitCol='\t'
splitRow='\n'
dayWeek=1 ## 下周星期1 处理
data = None
headers = None

def main():
    global data, headers
    dealday=getDealDay(_dealday)
    excelBuilder = Comm.ExcelBuilder.ExcelBuilder(path)
    data=excelBuilder.readSheet(1,fromX=1,fromY=1,returnType="字典")
    if data is not None:
        excelBuilder.delByIndex(17)  #删除 "歌曲语言"
        excelBuilder.delByIndex(9)   #删除 "彩铃ID"
        excelBuilder.delByIndex(9)   #删除 "歌曲ID"

        excelBuilder.insertByIndex(9,'')
        excelBuilder.insertByIndex(9, dealday)
        excelBuilder.insertByIndex(9, '已完结')
        excelBuilder.insertByIndex(9, '')
        excelBuilder.insertByIndex(9, '')
        data=excelBuilder.getData()
        headers=excelBuilder.getHeader()
        exportFile(newPath)
       # os.system('sh insertHive.sh {0} {1}'.format(newPath, targetTable))

def getDealDay(_dealday):
    '''
    得到处理日
    :param _dealday: 
    :return: 
    '''
    dateBuilder = Comm.DateBuilder.DateBuilder()
    weekTuple = dateBuilder.getweekmsg(_dealday)  # 第几周
    newWeek =weekTuple[1]+1 ##下周处理，所以加1周
    dayList = dateBuilder.getWeekDays('{0}{1}'.format(weekTuple[0], newWeek))  # 周的起始时间
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









if __name__=="__main__":

    main()