# coding=UTF-8
import random
import traceback

import datetime

import sys   #解决乱码问题
reload(sys)   #解决乱码问题

class DateBuilder:
    def __init__(self):
        pass

    def getweekmsg(self,strdate):
        '''
        查询某个日期是第多少周
        :param strdate: 日期（如：'20170701'）
        :return: 第几周
        '''
        _datetime = datetime.datetime.strptime(strdate, '%Y%m%d')
        weekmsg = _datetime.isocalendar()
        return weekmsg

    def getWeekDays(self,weekflag):
        '''
        传周数，返回周的日期列表
        :param weekflag: 周数（如：201720）
        :return: 列表
        '''
        yearnum = weekflag[0:4]  # 取到年份
        weeknum = weekflag[4:6]  # 取到周
        stryearstart = yearnum + '0101'  # 当年第一天
        yearstart = datetime.datetime.strptime(stryearstart, '%Y%m%d')  # 格式化为日期格式
        yearstartcalendarmsg = yearstart.isocalendar()  # 当年第一天的周信息
        yearstartweek = yearstartcalendarmsg[1]
        yearstartweekday = yearstartcalendarmsg[2]
        yearstartyear = yearstartcalendarmsg[0]
        if yearstartyear < int(yearnum):
            daydelat = (8 - int(yearstartweekday)) + (int(weeknum) - 1) * 7
        else:
            daydelat = (8 - int(yearstartweekday)) + (int(weeknum) - 2) * 7
        result = [];
        a = (yearstart + datetime.timedelta(days=daydelat)).date()
        for i in range(7):
            result.append((a + datetime.timedelta(days=i)).strftime('%Y%m%d'))
        return result