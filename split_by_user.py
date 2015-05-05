#-*-coding:utf-8-*-

"""
遍历'data/date/'目录下的所有csv文件，按照用户分割，生成'data/user'目录以及用户文件.

用户文件内容格式：

'date','item_id','behavior_type','user_geohash','item_category','hour'

"""

import os
import csv
import time

#记录已存在的user_id.csv
user_dictionary = {}



def writeByUser(user_id,words):
    file_name = user_id+".csv"
    os.chdir("E:/Niulab/EMC/EMCdata/user/")
    if not user_dictionary.has_key(user_id):
        user_dictionary[user_id] = True
        f = open(file_name,'ab')
        write = csv.writer(f)
        write.writerow(['location','start_time','duration','ISP','ToS','domain name','Bytes in Communication','HTTP request number'])
        # ISP: Internet Service Provider     ToS: Type of Service
        write.writerow(words)
        f.close()
    else:
        f = open(file_name,'ab')
        write = csv.writer(f)
        write.writerow(words)
        f.close()
    os.chdir("E:/Niulab/EMC/github/emc-sjtu/")


def splitByUser():
    os.mkdir("E:/Niulab/EMC/EMCdata/user/")
    f = open("E:/Niulab/EMC/EMCdata/net_traffic_sample.csv")
    rows = csv.reader(f)
    # rows.next()
    for row in rows:
        user_id = row[0]
        words = row[1:]
        writeByUser(user_id,words)


