# @@ -0,0 +1,32 @@
# -*-coding:utf-8-*-
#coding=utf-8
"""
function introduction:
1.data cleaning:remove all NULL byte from the orignal dataset
2.run splitByUser function in 'split_by_user.py', split the dataset based on user_id and storage small set in "/EMCdata/user/"
3.run generateDictBy(para) function in 'emcdata_split.py' to generate one dictionary and two sets.
    if para == 'CommunicationTotalByte':    dictionary = {(user_id,web):Byte}       here 'Byte' represents the user's total communication bytes number on this web
    if para == 'Duration':  dictionary = {(user_id,web):'dur'}         here 'dur' represents the user's total visiting time on this web
    if para == 'HTTPRequestNum':    dictionary = {(user_id,web):'HTTP_request'}     here 'HTTP_request' represents how many HTTP request the user has made on this web
    if para == 'VisitingNum':       dictionary = {(user_id,web):'visit_num'}     here 'visit_num' represents the total number that the user has visited this web
4.the returned value of this function is a dictionary which contains the corresponding'.pkl' files' path
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
    # splitByUser()
    t2 = time.time()
    print "It takes %f s to split by user,generate '/user/*.csv'" %(t2-t1)
    path = generateDictBy(value_style)
    t3 = time.time()
    print "It takes %f s to split by user and ISP,generate dictionary" %(t3-t2)
    print "====================================="
    return path


if __name__ == '__main__':
    data_preprocess('CommunicationTotalByte')
    data_preprocess('Duration')
    data_preprocess('HTTPRequestNum')
    data_preprocess('VisitingNum')