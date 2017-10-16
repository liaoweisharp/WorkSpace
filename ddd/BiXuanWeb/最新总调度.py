# coding=GBK
import os
import logger
import sys
reload(sys)
sys.setdefaultencoding('gbk')
logger.logger.info("----- step 1 最新工程项目.py --------")
os.system("python 最新工程项目.py")
logger.logger.info("-----  step 2 最新工程项目_Step2_人员业绩.py --------")
os.system("python D:\Python27\WorkSpace\ddd\BiXuanWeb\最新工程项目_Step2_人员业绩.py")
logger.logger.info("-----  step 3 最新项目满意度.py --------")
os.system("python D:\Python27\WorkSpace\ddd\BiXuanWeb\最新项目满意度.py")
logger.logger.info("-----  step 4 最新项目满意度_个人.py --------")
os.system("python D:\Python27\WorkSpace\ddd\BiXuanWeb\最新项目满意度_个人.py")
