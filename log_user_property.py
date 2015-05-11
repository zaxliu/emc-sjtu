#coding=utf-8
import csv
import os
import cPickle
import numpy as np
from log_user_trade import accountPick

# storage user property including 'userID','sex','birthday','grade','type of student' and 'account' into a matrix
def userPropertyPick(net_users_path, net_account_path, net_trade_path, uid_list):
    print "generating user property matrix"
    pro_parh = net_users_path+".userproperty/"
    f = open(net_users_path,'r+')
    rows = csv.reader(f)
    new_dict = {}
    user_pro_matrix = []
    account_dict = accountPick(net_account_path, net_trade_path)
    for row in rows:
        if account_dict.has_key(row[0]):
            account_value = account_dict[row[0]]
            type_of_stu = account_value[0]
            amount = account_value[1]
            row.append(type_of_stu)
            row.append(amount)
        else:
            row.append('no information')
            row.append(-1)
        new_dict[row[0]] = row[1:]

    for uid in uid_list:
        uid_pro = [uid] + new_dict[uid]
        user_pro_matrix.append(uid_pro)
    if not os.path.exists(pro_parh):
        os.mkdir(pro_parh)
    f_pro = open(pro_parh+"user_property.pkl", 'wb')
    cPickle.dump(user_pro_matrix, f_pro, -1)
    f_pro.close()
    path = {'user_property':pro_parh+"user_property.pkl"}
    print "finish"
    return path

if __name__ == '__main__':
    uid_list = cPickle.load(open("../EMCdata/net_traffic.dat.dictionary/userID_list.pkl", 'rb'))
    userPropertyPick('../EMCdata/net_users.dat','../EMCdata/account.txt','../EMCdata/trade.txt', uid_list)