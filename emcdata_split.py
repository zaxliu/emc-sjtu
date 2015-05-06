#coding=utf-8
import csv

# 从原始数据中提取出userID和user访问的web，分别用两个set存储userID和userWeb的信息。然后生成一个Dictionary，其中的key是由userID和userWeb组合成的一个tuple，value是该用户访问该网站的总时长。
final_dictionary = {}
userid_set = set([])
ISP_set = set([])

def addTuple(user_id,isp,byte):
    userid_set.add(user_id)
    ISP_set.add(isp)
    key_tuple = (user_id,isp)
    if not final_dictionary.has_key(key_tuple):
        final_dictionary[key_tuple] = byte
    else:
        final_dictionary[key_tuple] = final_dictionary[key_tuple] + byte


def splitByUserandWeb():
    f = open("E:/Niulab/EMC/EMCdata/net_traffic_sample.csv")
    rows = csv.reader(f)
    for row in rows:
        user_id = row[0]
        ISP_total = row[4].split(";")
        Com_byte = row[7].split(";")
        for index,isp in enumerate(ISP_total):
            print isp
            addTuple(user_id,isp,Com_byte[index])
    print final_dictionary
