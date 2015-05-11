# -*-coding:utf8-*-
"""
Main script

This is the main script that glues the modules together
"""
from sklearn.cluster import KMeans
from sklearn import metrics
from gen_profile_vector import full_profile_vector
from log_preprocess import log_preprocess
import numpy as np
import cPickle
import time
import matplotlib.pyplot as plt
from clustering import gen_feature_matrix
from clustering import do_clustering

# Preprocess logs
net_traffic_path = "../EMCdata/net_traffic.dat"
net_users_path = "../EMCdata/net_users.dat"
net_account_path = "../EMCdata/account.txt"
net_trade_path = "../EMCdata/trade.txt"
value_style = 'CommunicationTotalByte'
# profile_path = log_preprocess(net_traffic_path, net_users_path, net_account_path, net_trade_path, value_style)
# profile_path = net_traffic_path+".profile/profile_(user,domain)-TotalBytes.pkl"  # Uncomment to use generated files
# profile_path = net_traffic_path+".profile/profile_(user,domain)-Duration.pkl"
# profile_path = net_traffic_path+".profile/profile_(user,domain)-RequestNum.pkl"
profile_path = net_traffic_path+".profile/profile_(user,domain)-VisitingNum.pkl"
pid_path = net_traffic_path+".profile/pid.pkl"

# Generate feature matrix
feature_style = "TFIDF_LSA"
print profile_path,
print feature_style
feature_pkl_path = gen_feature_matrix(net_traffic_path=net_traffic_path, profile_path=profile_path,feature_style=feature_style)

# Do clustering and get index
K = 10
options = {'feature_style': feature_style, 'method': 'k-means++', 'K': K, 'n_init': 10}
index = do_clustering(net_traffic_path=net_traffic_path,feature_pkl_path=feature_pkl_path, options=options)

# Visualize cluster property
viz_profile_path = net_traffic_path+".profile/profile_(user,domain)-TotalBytes.pkl"
profile = cPickle.load(open(viz_profile_path, 'rb'))  # original profile vector
pid_list = list(cPickle.load(open(pid_path, 'rb')))
num_u, num_p = profile.shape

viz_userproperty_path = net_users_path+".userproperty/user_property.pkl"
uid_path = net_traffic_path+".profile/uid.pkl"
userproperty = cPickle.load(open(viz_userproperty_path, 'rb'))  # user_property_matrix, 0 for F, 1 for M.

avgProfile = np.zeros([K, num_p])
num_u_c = np.zeros([K])
totalBytes = np.zeros([K])

num_u_c_undergraduate = np.zeros([K])
num_u_c_MS = np.zeros([K])
num_u_c_PHD = np.zeros([K])
num_u_c_jiaogong = np.zeros([K])
avgAmount = np.zeros([K])

userproperty = np.array(userproperty)
age_vector = userproperty[:, 2]
age_list = sorted(list(set(age_vector)))
print age_list
num_age = len(age_list)
disAge = np.zeros([K, num_age])

year_enroll_vector = userproperty[:, 3]
year_enroll = sorted(list(set(year_enroll_vector)))
print year_enroll
num_year = len(year_enroll)
disYear = np.zeros([K, num_year])

for u in range(num_u):
    label = index[u]
    avgProfile[label, :] += profile[u, :]/np.sum(profile[u, :])
    totalBytes[label] += np.sum(profile[u, :])
    num_u_c[label] += 1

    #print userproperty[u],
    #print userproperty[u][4].decode('utf-8')
    avgAmount[label] += float(userproperty[u][5])
    if userproperty[u][4] == '\xe6\x9c\xac\xe7\xa7\x91':  # undergraduate
        num_u_c_undergraduate[label] += 1
    elif userproperty[u][4] == '\xe7\xa1\x95\xe5\xa3\xab':  # MS
        num_u_c_MS[label] += 1
    elif userproperty[u][4] == '\xe5\x8d\x9a\xe5\xa3\xab':  # PHD
        num_u_c_PHD[label] += 1
    else:
        num_u_c_jiaogong[label] += 1

    disAge[label][age_list.index(age_vector[u])] += 1
    disYear[label][year_enroll.index(year_enroll_vector[u])] += 1

for k in range(K):
    avgAmount[k] /= num_u_c[k]
    num_u_c_undergraduate[k] /= num_u_c[k]
    num_u_c_MS[k] /= num_u_c[k]
    num_u_c_PHD[k] /= num_u_c[k]
    num_u_c_jiaogong[k] /= num_u_c[k]
    avgProfile[k, :] /= num_u_c[k]
    disAge[k, :] /= num_u_c[k]
    disYear[k, :] /= num_u_c[k]

    top_domains = []
    top_domains_idx = avgProfile[k, :].argsort()[::-1][0:10]
    for idx in top_domains_idx:
        top_domains.append(pid_list[idx])
    print k+1,
    print '(%d users, %.3f GB, %.3f MB/user)' % (num_u_c[k], 1.0*totalBytes[k]/10.0**9,(1.0*totalBytes[k]/10.0**6)/num_u_c[k]),
    print ': '
    for domain in top_domains:
        print domain.decode('utf-8'),
        print '|',
    print '...'
    plt.figure("fig_domain")
    plt.subplot2grid([K, 1], (k, 0), 1, 1)
    plt.plot(np.arange(num_p), avgProfile[k, :])
    plt.figure("fig_disAge")
    plt.subplot2grid([K, 1], (k, 0), 1, 1)
    plt.plot(age_list, disAge[k, :])
    plt.figure("fig_disYear_enrollment")
    plt.subplot2grid([K, 1], (k, 0), 1, 1)
    plt.plot(year_enroll, disYear[k, :])
plt.figure("fig_amount")
plt.plot(range(K), avgAmount)
plt.figure("fig_undergraduate")
plt.plot(range(K), num_u_c_undergraduate)
plt.figure("fig_MS")
plt.plot(range(K), num_u_c_MS)
plt.figure("fig_PHD")
plt.plot(range(K), num_u_c_PHD)
plt.figure("fig_jiaogong")
plt.plot(range(K), num_u_c_jiaogong)
plt.show()
#
