#coding=utf-8
import csv
import os
import cPickle

# 从原始数据中提取出userID和user访问的web，分别用两个set存储userID和userWeb的信息。然后生成一个Dictionary，其中的key是由userID和userWeb组合成的一个tuple，value是该用户访问该网站的总时长。
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


def generateDictBy(para):
    f = open("../EMCdata/net_traffic_sample.csv")
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
                addTupleandByte(user_id, isp, Com_byte[index])
    cPickle.dump(final_dictionary,f_dict, -1)
    f_dict.close()
    cPickle.dump(userid_set,f_user, -1)
    f_user.close()
    cPickle.dump(ISP_set,f_ISP, -1)
    f_ISP.close()
    path = {'userID': '../EMCdata/Dictionary/ISP_set.pkl','visiting_ISP': '../EMCdata/Dictionary/ISP_set.pkl',para: '../EMCdata/Dictionary/'+para+'.pkl'}
    return path
