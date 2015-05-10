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
profile_path = net_traffic_path+".profile/profile_(user,domain)-TotalBytes.pkl"  # Uncomment to use generated files
pid_path = net_traffic_path+".profile/pid.pkl"

# Generate feature matrix
feature_style = "TFIDF_LSA"
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

avgProfile = np.zeros([K, num_p])
num_u_c = np.zeros([K])
totalBytes = np.zeros([K])

for u in range(num_u):
    label = index[u]
    avgProfile[label, :] += profile[u, :]/np.sum(profile[u, :])
    totalBytes[label] += np.sum(profile[u, :])
    num_u_c[label] += 1
for k in range(K):
    avgProfile[k, :] /= num_u_c[k]
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
    plt.subplot2grid([K, 1], (k, 0), 1, 1)
    plt.plot(np.arange(num_p), avgProfile[k, :])
plt.show()
#
