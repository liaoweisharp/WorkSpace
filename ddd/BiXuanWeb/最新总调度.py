# coding=GBK
import os
import logger
import sys
reload(sys)
sys.setdefaultencoding('gbk')
logger.logger.info("----- step 1 ���¹�����Ŀ.py --------")
os.system("python ���¹�����Ŀ.py")
logger.logger.info("-----  step 2 ���¹�����Ŀ_Step2_��Աҵ��.py --------")
os.system("python D:\Python27\WorkSpace\ddd\BiXuanWeb\���¹�����Ŀ_Step2_��Աҵ��.py")
logger.logger.info("-----  step 3 ������Ŀ�����.py --------")
os.system("python D:\Python27\WorkSpace\ddd\BiXuanWeb\������Ŀ�����.py")
logger.logger.info("-----  step 4 ������Ŀ�����_����.py --------")
os.system("python D:\Python27\WorkSpace\ddd\BiXuanWeb\������Ŀ�����_����.py")
