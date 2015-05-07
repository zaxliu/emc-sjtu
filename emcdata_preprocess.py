# @@ -0,0 +1,32 @@
# -*-coding:utf-8-*-
#coding=utf-8
"""
本函数包含以下功能：
1.对原始数据进行清洗，消除里面的所有NULL字符
2.运行split_by_user.py中对应的分割函数，在user目录下生成按用户区分的文件
3.运行emcdata_split.py中的生成Dict的函数，函数输入为需要分割的方式，根据分割方式在/EMCdata/Dictionary/目录下存储set和dictionary，输出为pkl文件对应的路径
"""
import time
from delete_space import deleteSpace
from split_by_user import splitByUser
# from gen_iid_geohash_category import genIid
# from gen_uid_iid import genUidIid
from emcdata_split import generateDictBy

# value_style could be: Duration,CommunicationTotalByte,HTTPRequestNum,VisitingNum
def data_preprocess(value_style):
    print "====================================="
    t0 = time.time()
    deleteSpace()
    t1 = time.time()
    print "It takes %f s to delete all spaces and generate 'EMC/EMCdata/*.csv'" %(t1-t0)
    splitByUser()
    t2 = time.time()
    print "It takes %f s to split by user,generate '/user/*.csv'" %(t2-t1)
    path = generateDictBy(value_style)
    t3 = time.time()
    print "It takes %f s to split by user and ISP,generate dictionary" %(t3-t2)
    print "====================================="
    return path


print data_preprocess('CommunicationTotalByte')