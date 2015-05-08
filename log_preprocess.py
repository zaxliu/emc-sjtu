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
from log_delete_null import delete_null
from log_split_by_user import splitByUser
from log_gen_dict import generateDictBy

# value_style could be: Duration,CommunicationTotalByte,HTTPRequestNum,VisitingNum
def log_preprocess(net_traffic_path, value_style):
    print "====================================="
    t0 = time.time()
    # delete_null(net_traffic_path)
    t1 = time.time()
    print "It takes %f s to delete all NULLs" %(t1-t0)
    # splitByUser(net_traffic_path)
    t2 = time.time()
    print "It takes %f s to split log by user" %(t2-t1)
    path = generateDictBy(net_traffic_path, value_style)
    t3 = time.time()
    print "It takes %f s to generate dictionary" %(t3-t2)
    print "====================================="
    return path


if __name__ == '__main__':
    log_preprocess('CommunicationTotalByte')
    log_preprocess('Duration')
    log_preprocess('HTTPRequestNum')
    log_preprocess('VisitingNum')