# coding=UTF-8
import traceback


import cx_Oracle
import sys   #解决乱码问题

from logger import logger

reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题

class DatabaseDAL:
    def __init__(self,host="10.25.163.26",user="migu",password="migu213",database="migudw"):
        '''
        构造函数
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
        self.conn = cx_Oracle.connect('{0}/{1}@{2}/{3}'.format(self.user,self.password,self.host,self.database))
        #self.conn = cx_Oracle.connect(host=self.host, user=self.user, password=self.password, database=self.database)
        self.cur = self.conn.cursor()
    def insert(self,tableName,list,sequenceList=[]):
        '''
        插入表
        :param tableName: 表名
        :param list: 列表，元素为字典，字典的键是字段名
        :param sequenceList: 列表，sequence列表，如：["id"]
        :return: 成功插入的个数
        '''

        result=0;
        if len(list)<=0:
            return result
        try:
            logger.info("共{0}个记录，入库中......".format(len(list)).decode("utf8"))
            sequenceIndexes=None



            for dic in list:
                sqlList = [];
                sqlList.append(" insert into {0}(".format(tableName))
                if len(dic.items())<=0:
                    continue

                if len(sequenceList)>0 and sequenceIndexes is None:
                    sequenceIndexes=[]
                    index=0
                    for key in dic.keys():
                        try:
                            if key in sequenceList:
                                sequenceIndexes.append(index)
                        except:
                            traceback.print_exc()
                        finally:
                            index+=1
                sqlList.append(",".join(dic.keys()))
                sqlList.append(")")
                sqlList.append(" values(")
                keyList=[]
                keys={}
                for key in dic.keys():
                    if key not in sequenceList:
                        #不是序列
                        keyList.append(":"+key)
                        keys[key]=dic[key]
                    else:
                        #是个序列
                        keyList.append(dic[key]+".Nextval")
                valuestr=",".join(keyList)
                sqlList.append(valuestr)
                sqlList.append(")")
                sql = "".join(sqlList)
                self.cur.execute(sql,keys)
                valueList = []
                # index=0
                # for value in dic.values():
                #     #判断字符串类型，打上单引号
                #     if sequenceIndexes is not None and index in sequenceIndexes:
                #         value="{0}.Nextval".format(value)
                #         valueList.append(value)
                #     elif isinstance(value,(unicode,str)):
                #         value= value.replace('\'','\'\'');
                #         valueList.append("%s"%value)
                #     else:
                #         valueList.append(value)
                #     index +=1
                # sqlList.append(",".join(map(str, valueList)))
                # sqlList.append(")")
                # sql="".join(sqlList)
                # sql=sql.replace("\\","")
                # self.cur.execute(sql)   #执行插入
            self.conn.commit()
        except Exception,e:
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
            logger.info("共{0}个记录，更新中......".format(len(list)).decode("utf8"))
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


                    setList.append("{0}=:{0}".format(obj[0]))
                for where in whereTuple:
                    whereList.append("{0}=:{0}".format(where))
                sqlList.append(" {0}".format(",".join(setList)))
                sqlList.append(" where {0}".format(" and ".join(whereList)))
                sql="".join(sqlList)
                self.cur.execute(sql,dic)   #执行插入
            self.conn.commit()
        except:
            traceback.print_exc()
            logger.error("---- SQL-----")
            print sql
            # self.dispose()
            result=-1
        else:
            logger.info("共{0}个记录，更新结束".format(len(list)).decode("utf8"))
        finally:

            return result
    # def update(self,tableName,list,whereTuple):
    #     '''
    #     更新表
    #     :param tableName: 表名
    #     :param list: 列表，元素为字典，字典的键是字段名
    #     :param whereTuple: where条件元组
    #     :return: 更新个数
    #     '''
    #
    #     result=0;
    #     if len(list)<=0:
    #         return result
    #     sql=""
    #     try:
    #         logger.info("共{0}个记录，更新中......".format(len(list)).decode("utf8"))
    #         for dic in list:
    #             sqlList = [];
    #             sqlList.append(" update {0} set ".format(tableName))
    #             setList=[]
    #             whereList=[]
    #             if len(dic.items())<=0:
    #                 continue
    #             for obj in dic.items():
    #                 if obj[0] in whereTuple:
    #                     # 是where的关键字，则跳过
    #                     continue
    #                 if isinstance(obj[1], (unicode, str)):
    #                     val=obj[1].replace("'", "''") #如果是字符串，则去掉替换掉单引号（讲究sqlserver的转义）
    #                 else:
    #                     val = obj[1]
    #
    #                 setList.append("{0}='{1}'".format(obj[0],val))
    #             for where in whereTuple:
    #                 if isinstance(dic[where], (unicode, str)):
    #                     whereValue=dic[where].replace("'", "''")
    #                 else:
    #                     whereValue =dic[where]
    #                 whereList.append("{0}='{1}'".format(where,whereValue))
    #             sqlList.append(" {0}".format(",".join(setList)))
    #             sqlList.append(" where {0}".format(" and ".join(whereList)))
    #             sql="".join(sqlList)
    #             self.cur.execute(sql)   #执行插入
    #         self.conn.commit()
    #     except:
    #         traceback.print_exc()
    #         logger.error("---- SQL-----")
    #         print sql
    #         # self.dispose()
    #         result=-1
    #     else:
    #         logger.info("共{0}个记录，更新结束".format(len(list)).decode("utf8"))
    #     finally:
    #
    #         return result
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

