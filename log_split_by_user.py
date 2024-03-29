#-*-coding:utf-8-*-

"""
读取'EMC/EMCdata/net_traffic_nospace.csv'文件，按照用户分割，生成'data/user'目录以及用户文件.

用户文件内容格式：

'date','item_id','behavior_type','user_geohash','item_category','hour'

"""

import os
import csv
import time

#记录已存在的user_id.csv
user_dictionary = {}


def writeByUser(user_log_path, user_id, words):
    file_name = user_log_path + user_id+".csv"
    if not user_dictionary.has_key(user_id):
        user_dictionary[user_id] = True
        f = open(file_name,'ab')
        write = csv.writer(f)
        write.writerow(['location','start_time','duration','domain','ToS','domain name','Bytes in Communication','HTTP request number'])
        # ISP: Internet Service Provider     ToS: Type of Service
        write.writerow(words)
        f.close()
    else:
        f = open(file_name,'ab')
        write = csv.writer(f)
        write.writerow(words)
        f.close()


def splitByUser(net_traffic_path):
    user_log_path = net_traffic_path+".user/"
    if not os.path.exists(user_log_path):
        os.mkdir(user_log_path)
    f = open(net_traffic_path+".nonull")
    rows = csv.reader(f)
    # rows.next()
    for row in rows:
        user_id = row[0]
        words = row[1:]
        writeByUser(user_log_path, user_id, words)


