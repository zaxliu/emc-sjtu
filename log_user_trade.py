#coding=utf-8

import os
import csv
dictionary = {}

def addtrade(cardID, amount):
    if not dictionary.has_key(cardID):
        dictionary[cardID] = amount
    else:
        dictionary[cardID] += amount

# pick up each user's total amount of consumption. return dictionary = {cardID: amount}
def tradePick(net_trade_path):
    print "start trade message picking up"
    f = open(net_trade_path, 'r+')
    f.readline()
    line = f.readline()
    while line:
        message = line.split()
        cardID = message[0]
        amount = float(message[5])
        addtrade(cardID, amount)
        line = f.readline()
    f.close()
    print "finish trad message picking up"
    return dictionary

# match cardID and userID, return dictionary = {userID:[type_of_student,amount]}
def accountPick(net_account_path, net_trade_path):
    print "matching cardID and userID"
    dictionary = tradePick(net_trade_path)
    new_dict = {}
    f = open(net_account_path, 'r+')
    f.readline()
    line = f.readline()
    while line:
        message = line.split()
        cardID = message[0]
        userID = message[1]
        type_of_stu = message[5]
        if dictionary.has_key(cardID):
            trade = dictionary[cardID]
            new_dict[userID] = [type_of_stu, trade]
        line = f.readline()
    print "finish matching"
    return new_dict

accountPick("../EMCdata/account.txt", "../EMCdata/trade.txt")