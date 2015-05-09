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

# Preprocess logs
net_traffic_path = "../EMCdata/net_traffic.dat"
value_style = 'CommunicationTotalByte'
# dict_path = log_preprocess(net_traffic_path, value_style)
# Uncomment the following to use generated files
dict_path = {'userID': net_traffic_path+".dictionary/userID_set.pkl",
        'domain': net_traffic_path+".dictionary/domain_set.pkl",
        'method': net_traffic_path+".dictionary/"+value_style+".pkl"}

# Generate profile vector
profile_path = full_profile_vector(net_traffic_path=net_traffic_path, pkl_path=dict_path, option='Origin')
# Uncomment the following to use generated files
# profile_path = net_traffic_path+".profile_vector/profile.pkl"
# profile = cPickle.load(open(profile_path, 'rb'))

# # Do clustering and show performance (inertia)
# max_K = 5
# num_run = 1
# inertia = np.zeros([max_K, num_run])
# print "K, run, time, Inertia"
# for idx_K, K in enumerate(np.arange(max_K)+1):
#     for run_id in range(num_run):
#         t = time.time()
#         model = KMeans(n_clusters=K, init='k-means++', n_init=1)   # initialize model
#         model.fit(profile)    # train model
#         inertia[idx_K, run_id] = model.inertia_
#         print "%1d, %3d, %.2f, %.6f" % (K, run_id, time.time()-t, model.inertia_)
#
# plt.plot(np.array(range(max_K))+1, inertia.mean(axis=1))
# plt.show()
# pass

# # Get average user profile of each cluster
# iid_list = list(cPickle.load(open(dict_path['domain'], 'rb')))
# K = 6
# num_u, num_f = profile.shape
# model = KMeans(n_clusters=K, init='k-means++', n_init=1)
# model.fit(profile)
# avgProfile = np.zeros([K, num_f])
# num_u_c = np.zeros([K])
# for u in range(num_u):
#     label = model.labels_[u]
#     if np.sum(profile[u, :]) ==0:
#         pass
#     avgProfile[label, :] += profile[u, :]
#     num_u_c[label] += 1
# for k in range(K):
#     avgProfile[k, :] /= num_u_c[k]
#     top_domains = []
#     top_domains_idx = avgProfile[k, :].argsort()[::-1][0:5]
#     for idx in top_domains_idx:
#         top_domains.append(iid_list[idx])
#     print k,
#     print ': '
#     for domain in top_domains:
#         print domain.decode('utf-8'),
#     print '\n'
#     plt.subplot2grid([K, 1], (k, 0), 1, 1)
#     plt.plot(np.arange(num_f), avgProfile[k, :])
# plt.show()
# pass
#
