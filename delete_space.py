#coding=utf-8

import os
import csv


# 删除掉原文件中的所有空格字符，空格会导致后续csv读取时报错
def deleteSpace():
    f = open("../EMCdata/net_traffic.dat", 'r+')
    filename = "../EMCdata/net_traffic_nospace.csv"
    f_new = open(filename, 'w')
    num = 1
    line = f.readline()
    while line:
        # newline = line.replace(' ', '')
        newline = line.replace('\x00', '')
       # for index,each_string in enumerate(split_line):
       #     split_line[index] = each_string.replace('百度','替换')
       #     split_line[index] = each_string.replace('\n','')
       # print split_line
       # write = csv.writer(f_new)
        # write.writerow(line)
        f_new.write(newline)
        line = f.readline()
    f_new.close()