# coding=UTF-8
import sys   #解决乱码问题

reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题

def strConvertDic(str,itemSplit=';',keySplit='='):
    '''
    字符串转字典类型
    :param str: 字符串
    :param itemSplit: 分隔符，如：逗号
    :param keySplit: 键值分隔符，如：等号
    :return: 字典
    '''
    cookies = {}  # 初始化cookies字典变量
    for line in str.split(itemSplit):
       # 其设置为1就会把字符串拆分成2份
       name, value = line.strip().split(keySplit, 1)
       cookies[name] = value
    return cookies;