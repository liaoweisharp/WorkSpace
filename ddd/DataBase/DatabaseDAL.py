# coding=UTF-8
import traceback

import pymssql
import sys   #解决乱码问题

from logger import logger

reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题

class DatabaseDAL:
    def __init__(self,host=".",user="sa",password="liaowei",database="ZiZhi",charset='utf8'):
        '''
        构造 函数
        :param host: 
        :param user: 
        :param password: 
        :param database: 
        :param charset: 
        '''
        self.host=host
        self.user=user
        self.password=password
        self.database=database
        self.chartset=charset
        self.conn = pymssql.connect(host=self.host, user=self.user, password=self.password, database=self.database, charset=self.chartset)
        self.cur = self.conn.cursor()
    def insert(self,tableName,list):
        '''
        插入表
        :param tableName: 表名
        :param list: 列表，元素为字典，字典的键是字段名
        :return: 成功插入的个数
        '''

        result=0;
        if len(list)<=0:
            return result
        try:
            logger.info("共{0}个记录，入库中......".format(len(list)).decode("utf8"))
            for dic in list:
                sqlList = [];
                sqlList.append(" insert into {0}(".format(tableName))
                if len(dic.items())<=0:
                    continue
                sqlList.append(",".join(dic.keys()))
                sqlList.append(")")
                sqlList.append(" values(")
                valueList=[]
                for value in dic.values():
                    #判断字符串类型，打上单引号
                    if isinstance(value,(unicode,str)):
                        value= value.replace('\'','\'\'');
                        valueList.append("N'{0}'".format(value))
                    else:
                        valueList.append(value)
                sqlList.append(",".join(map(str, valueList)))
                sqlList.append(")")
                sql="".join(sqlList)
                self.cur.execute(sql)   #执行插入
            self.conn.commit()
        except:
            traceback.print_exc()
            # self.dispose()
            result=-1
        else:
            logger.info("共{0}个记录，入库结束".format(len(list)).decode("utf8"))
        finally:

            return result
    def update(self,tableName,list,whereTuple):
        '''
        更新表
        :param tableName: 表名
        :param list: 列表，元素为字典，字典的键是字段名
        :param whereTuple: where条件元组
        :return: 更新个数
        '''

        result=0;
        if len(list)<=0:
            return result
        sql=""
        try:
            logger.info("共{0}个记录，入库更新中......".format(len(list)).decode("utf8"))
            for dic in list:
                sqlList = [];
                sqlList.append(" update {0} set ".format(tableName))
                setList=[]
                whereList=[]
                if len(dic.items())<=0:
                    continue
                for obj in dic.items():
                    if obj[0] in whereTuple:
                        # 是where的关键字，则跳过
                        continue
                    if isinstance(obj[1], (unicode, str)):
                        val=obj[1].replace("'", "''") #如果是字符串，则去掉替换掉单引号（讲究sqlserver的转义）
                    else:
                        val = obj[1]

                    setList.append("{0}='{1}'".format(obj[0],val))
                for where in whereTuple:
                    if isinstance(dic[where], (unicode, str)):
                        whereValue=dic[where].replace("'", "''")
                    else:
                        whereValue =dic[where]
                    whereList.append("{0}='{1}'".format(where,whereValue))
                sqlList.append(" {0}".format(",".join(setList)))
                sqlList.append(" where {0}".format(" and ".join(whereList)))
                sql="".join(sqlList)
                self.cur.execute(sql)   #执行插入
            self.conn.commit()
        except:
            traceback.print_exc()
            logger.error("---- SQL-----")
            print sql
            # self.dispose()
            result=-1
        else:
            logger.info("共{0}个记录，入库更新结束".format(len(list)).decode("utf8"))
        finally:

            return result
    def execute(self,sql):
        self.cur.execute(sql)
        self.conn.commit()
    def query(self,sql):
        '''
        查询
        :param sql: 
        :return: 返回元组集合
        '''
        self.cur.execute(sql)
        list = self.cur.fetchall()
        return list
    def dispose(self):
        '''
        销毁，释放数据库连接
        :return: 
        '''
        if self.cur is not None:
            self.cur.close()
            self.conn.close()

