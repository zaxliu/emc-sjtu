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
domain_set = set([])


def addTupleandByte(user_id,domain,byte):
    userid_set.add(user_id)
    domain_set.add(domain)
    key_tuple = (user_id,domain)
    if not final_dictionary.has_key(key_tuple):
        final_dictionary[key_tuple] = byte
    else:
        final_dictionary[key_tuple] += byte


def addTupleandDuration(user_id,domain,duration):
    userid_set.add(user_id)
    domain_set.add(domain)
    key_tuple = (user_id,domain)
    if not final_dictionary.has_key(key_tuple):
        final_dictionary[key_tuple] = duration
    else:
        final_dictionary[key_tuple] = final_dictionary[key_tuple] + duration


def addTupleandHTTP(user_id,domain,http):
    userid_set.add(user_id)
    domain_set.add(domain)
    key_tuple = (user_id,domain)
    if not final_dictionary.has_key(key_tuple):
        final_dictionary[key_tuple] = http
    else:
        final_dictionary[key_tuple] = final_dictionary[key_tuple] + http


def addTupleandVisitNum(user_id,domain):
    userid_set.add(user_id)
    domain_set.add(domain)
    key_tuple = (user_id,domain)
    if not final_dictionary.has_key(key_tuple):
        final_dictionary[key_tuple] = 1
    else:
        final_dictionary[key_tuple] += 1


# main function
def generateDictBy(net_traffic_path, value_style):
    f = open(net_traffic_path+".nonull")
    dict_path = net_traffic_path+".dictionary/"
    if not os.path.exists(dict_path):
        os.mkdir(dict_path)
    f_user = open(dict_path+"userID_set.pkl", 'wb')    # user write mode to overwrite existing pkl files
    f_domain = open(dict_path+"domain_set.pkl", 'wb')
    f_dict = open(dict_path+value_style+".pkl", 'wb')
    rows = csv.reader(f)
    if value_style == 'CommunicationTotalByte':
        for row in rows:
            user_id = row[0]
            domain_total = row[4].split(";")
            Com_byte = row[7].split(";")
            for index, domain in enumerate(domain_total):
                addTupleandByte(user_id, domain, float(Com_byte[index]))
    elif value_style == 'Duration':
        for row in rows:
            user_id = row[0]
            domain_total = row[4].split(";")
            mean_duration = float(row[3])/len(domain_total)
            for index, domain in enumerate(domain_total):
                addTupleandDuration(user_id, domain, mean_duration)
    elif value_style == 'HTTPRequestNum':
        for row in rows:
            user_id = row[0]
            domain_total = row[4].split(";")
            HTTPnum = row[8].split(";")
            for index, domain in enumerate(domain_total):
                http = float(HTTPnum[index])
                addTupleandHTTP(user_id, domain, http)
    elif value_style == 'VisitingNum':
        for row in rows:
            user_id = row[0]
            domain_total = row[4].split(";")
            for index, domain in enumerate(domain_total):
                addTupleandVisitNum(user_id, domain)
    cPickle.dump(final_dictionary, f_dict, -1)
    f_dict.close()
    cPickle.dump(userid_set, f_user, -1)
    f_user.close()
    cPickle.dump(domain_set, f_domain, -1)
    f_domain.close()
    path = {'userID': dict_path+"userID_set.pkl",
            'domain': dict_path+"domain_set.pkl",
            'method': dict_path+value_style+".pkl"}
    return path
