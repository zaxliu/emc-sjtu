#coding=utf-8
import csv
import os
import cPickle
import numpy as np
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


def addTupleandByte(user_id, domain, byte):
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
    f_user = open(dict_path+"userID_list.pkl", 'wb')    # user write mode to overwrite existing pkl files
    f_domain = open(dict_path+"domain_list.pkl", 'wb')
    f_dict = open(dict_path+value_style+".pkl", 'wb')
    rows = csv.reader(f)
    if value_style == 'CommunicationTotalByte':
        for row in rows:
            user_id = row[0]
            domain_total = row[4].split(";")
            service_total = row[5].split(";")
            Com_byte = row[7].split(";")
            for index, domain in enumerate(domain_total):
                domain = domain.replace('1', '')    #删除掉无关字符，如“百度1”中的字符“1”
                domain = domain.replace('2', '')
                domain = domain.replace('3', '')
                web = domain + service_total[index]
                addTupleandByte(user_id, web, float(Com_byte[index]))
    elif value_style == 'Duration':
        for row in rows:
            user_id = row[0]
            domain_total = row[4].split(";")
            service_total = row[5].split(";")
            mean_duration = float(row[3])/len(domain_total)/1000/60 #以分钟为单位
            for index, domain in enumerate(domain_total):
                domain = domain.replace('1', '')
                domain = domain.replace('2', '')
                domain = domain.replace('3', '')
                web = domain + service_total[index]
                addTupleandDuration(user_id, web, mean_duration)
    elif value_style == 'HTTPRequestNum':
        for row in rows:
            user_id = row[0]
            domain_total = row[4].split(";")
            service_total = row[5].split(";")
            HTTPnum = row[8].split(";")
            for index, domain in enumerate(domain_total):
                domain = domain.replace('1', '')
                domain = domain.replace('2', '')
                domain = domain.replace('3', '')
                web = domain + service_total[index]
                http = float(HTTPnum[index])
                addTupleandHTTP(user_id, web, http)
    elif value_style == 'VisitingNum':
        for row in rows:
            user_id = row[0]
            domain_total = row[4].split(";")
            service_total = row[5].split(";")
            for index, domain in enumerate(domain_total):
                domain = domain.replace('1', '')
                domain = domain.replace('2', '')
                domain = domain.replace('3', '')
                web = domain + service_total[index]
                addTupleandVisitNum(user_id, web)

    print "Generating profile vector(without normalization)"
    uid_list = list(userid_set)
    iid_list = list(domain_set)
    full = np.zeros((len(uid_list), len(iid_list)))
    N = len(final_dictionary.keys())
    n = 0
    step = 10
    for u, i in final_dictionary.keys():
        uid = uid_list.index(u)
        iid = iid_list.index(i)
        full[uid, iid] = final_dictionary[(u, i)]
        n += 1
        if int(1.0*n/N*100) == step:
            print "-%d" % (int(1.0*n/N*100)),
            step += 10
    print "Succeed"


    cPickle.dump(full, f_dict, -1)
    f_dict.close()
    cPickle.dump(uid_list, f_user, -1)
    f_user.close()
    cPickle.dump(iid_list, f_domain, -1)
    f_domain.close()
    path = {'userID': dict_path+"userID_list.pkl",
            'domain': dict_path+"domain_list.pkl",
            'method': dict_path+value_style+".pkl"}
    return path, uid_list

if __name__ == "__main__":
    generateDictBy("../EMCdata/net_traffic_sample.txt", 'Duration')
