#coding=utf-8

import os
import csv


# 删除掉原文件中的所有空格字符，空格会导致后续csv读取时报错
def delete_null(net_traffic_log_path):
    f = open(net_traffic_log_path, 'r+')
    filename = net_traffic_log_path+".nonull"
    f_new = open(filename, 'w')
    num = 1
    line = f.readline()
    while line:
        newline = line.replace('\x00', '')
        f_new.write(newline)
        line = f.readline()
    f_new.close()