#coding=utf-8
import csv
import os
import cPickle
"""
function introduction:
1. pick up 'userID' message and 'web' message from the dataset. storage them in two sets
2. generate different dictionary based on the input parameter 'para':
    if para == 'CommunicationTotalByte':    dictionary = {(user_id,web):Byte}       here 'Byte' represents the user's total communication bytes number on this web
    if para == 'Duration':  dictionary = {(user_id,web):'dur'}         here 'dur' represents the user's total visiting time on this web
    if para == 'HTTPRequestNum':    dictionary = {(user_id,web):'HTTP_request'}     here 'HTTP_request' represents how many HTTP request the user has made on this web
    if para == 'VisitingNum':       dictionary = {(user_id,web):'visit_num'}     here 'visit_num' represents the total number that the user has visited this web
4.the returned value of this function is a dictionary which contains the corresponding'.pkl' files' path
"""

final_dictionary = {}
userid_set = set([])
ISP_set = set([])

def addTupleandByte(user_id,isp,byte):
    userid_set.add(user_id)
    ISP_set.add(isp)
    key_tuple = (user_id,isp)
    if not final_dictionary.has_key(key_tuple):
        final_dictionary[key_tuple] = byte
    else:
        final_dictionary[key_tuple] = final_dictionary[key_tuple] + byte

def addTupleandDuration(user_id,isp,duration):
    userid_set.add(user_id)
    ISP_set.add(isp)
    key_tuple = (user_id,isp)
    if not final_dictionary.has_key(key_tuple):
        final_dictionary[key_tuple] = duration
    else:
        final_dictionary[key_tuple] = final_dictionary[key_tuple] + duration

def addTupleandHTTP(user_id,isp,http):
    userid_set.add(user_id)
    ISP_set.add(isp)
    key_tuple = (user_id,isp)
    if not final_dictionary.has_key(key_tuple):
        final_dictionary[key_tuple] = http
    else:
        final_dictionary[key_tuple] = final_dictionary[key_tuple] + http

def addTupleandVisitNum(user_id,isp):
    userid_set.add(user_id)
    ISP_set.add(isp)
    key_tuple = (user_id,isp)
    if not final_dictionary.has_key(key_tuple):
        final_dictionary[key_tuple] = 1
    else:
        final_dictionary[key_tuple] += 1

#main function
def generateDictBy(para):
    f = open("../EMCdata/net_traffic_nospace.csv")
    if not os.path.exists("../EMCdata/Dictionary/"):
        os.mkdir("../EMCdata/Dictionary/")
    f_user = open("../EMCdata/Dictionary/userID_set.pkl", 'ab')
    f_ISP = open("../EMCdata/Dictionary/ISP_set.pkl", 'ab')
    f_dict = open("../EMCdata/Dictionary/"+para+".pkl", 'ab')
    rows = csv.reader(f)
    if para == 'CommunicationTotalByte':
        for row in rows:
            user_id = row[0]
            ISP_total = row[4].split(";")
            Com_byte = row[7].split(";")
            for index,isp in enumerate(ISP_total):
                byte_num = float(Com_byte[index])
                addTupleandByte(user_id, isp, byte_num)
    elif para == 'Duration':
        for row in rows:
            user_id = row[0]
            ISP_total = row[4].split(";")
            mean_duration = float(row[3])/len(ISP_total)
            for index,isp in enumerate(ISP_total):
                addTupleandDuration(user_id, isp, mean_duration)
    elif para == 'HTTPRequestNum':
        for row in rows:
            user_id = row[0]
            ISP_total = row[4].split(";")
            HTTPnum = row[8].split(";")
            for index,isp in enumerate(ISP_total):
                http = float(HTTPnum[index])
                addTupleandHTTP(user_id, isp, http)
    elif para == 'VisitingNum':
        for row in rows:
            user_id = row[0]
            ISP_total = row[4].split(";")
            for index,isp in enumerate(ISP_total):
                addTupleandVisitNum(user_id, isp)
    cPickle.dump(final_dictionary,f_dict, -1)
    f_dict.close()
    cPickle.dump(userid_set,f_user, -1)
    f_user.close()
    cPickle.dump(ISP_set,f_ISP, -1)
    f_ISP.close()
    path = {'userID': '../EMCdata/Dictionary/ISP_set.pkl','visiting_ISP': '../EMCdata/Dictionary/ISP_set.pkl',para: '../EMCdata/Dictionary/'+para+'.pkl'}
    return path
