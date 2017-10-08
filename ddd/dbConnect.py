# coding=UTF-8
import pymssql
import sys   #解决乱码问题

reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题
conn=pymssql.connect(host='.',user='sa',password='liaowei',database='MiGu',charset='utf8')   #解决乱码问题

cur=conn.cursor()

# ##插入
# sql="insert into tab_Classify(cf_ParentId,cf_Name) values({0},'{1}')".format(1,"廖aaa")
# cur.execute(sql)
# conn.commit()

##查询
cur.execute('select * from tab_Classify')
list=cur.fetchall()
print "len={0}".format(len(list))
for record in list:
    print "c1={0},c2={1},c3={2}".format(record[0],record[1],record[2])

cur.close()
conn.close()
