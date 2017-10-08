# coding=UTF-8
class class1(object):
    '''
    类说明....
    '''
    def __init__(self,age,name='廖伟'):
        '''
        构造函数
        :param age: 年龄
        :param name: 姓名
        '''
        self.name=name
        self.age=age

    def print_info(self):
        '''
        打印变量
        :return: 无返回
        '''
        print "Hello Here is name={0}".format(self.name)
        print "Hello Here is age={0}".format(self.age)

