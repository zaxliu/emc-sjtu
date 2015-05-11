# -*-encoding:utf:8-*-
'''
Data visualization by Lewis
'''
__author__ = 'Lewis'

import numpy as np
import cPickle
import time
import matplotlib.pyplot as plt
from clustering import gen_feature_matrix
from clustering import do_clustering
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import normalize
from sklearn.preprocessing import scale
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD

##---- Define file paths --------
net_traffic_path = "../EMCdata/net_traffic.dat"
# profile_path = net_traffic_path+".profile/profile_(user,domain)-TotalBytes.pkl"
# profile_path = net_traffic_path+".profile/profile_(user,domain)-VisitingNum.pkl"
# profile_path = net_traffic_path+".profile/profile_(user,domain)-Duration.pkl"
profile_path = net_traffic_path+".profile/profile_(user,domain)-TotalBytes.pkl"
pid_path = net_traffic_path+".profile/pid_(user,domain).pkl"  # Column ID of raw profile matrix

# ------Load supplementary variable
pid_list = list(cPickle.load(open(pid_path, 'rb')))

# ---- Statistics of raw profile ---------
profile_matrix = cPickle.load(open(profile_path, 'rb'))
col_mean = profile_matrix.mean(axis=0)
col_med = np.median(profile_matrix, axis=0)
row_mean = profile_matrix.mean(axis=1)
row_med = np.median(profile_matrix, axis=1)
# 查看stop-domain的情况
for i, idx in enumerate(np.argsort(col_med)[-1:-100:-1]):    # 依column median中倒序查看domain
    # plt.hist(np.log10(1+np.sort(profile_matrix[:, idx])[::-1]))    # 查看用户访问该domain的分布情况
    print i,                                                      # median排序序号
    print col_med[idx],
    print np.sum(profile_matrix[:, idx]==0.0),                    # 没有访问该网站的用户数
    print pid_list[idx].decode('utf-8')                          # domain 名称
    # plt.show()

# ---- Statistics of tf-idf ---------
# profile_matrix = np.log10(1+profile_matrix)
ti_trans = TfidfTransformer(use_idf=True, smooth_idf=True, sublinear_tf=True, norm='l2')
feature = ti_trans.fit_transform(profile_matrix).toarray()
# 查看前10个用户值最大的几个域名
# for u in range(feature.shape[0])[0:10]:
#     domain_order = np.argsort(feature[u, :])[-1:-20:-1]
#     for d in domain_order:
#         print pid_list[d].decode('utf-8'),
#     print('...')
#     plt.plot(feature[u, :])
#     plt.show()

# ---- Statistics of LSA---------
t_svd = TruncatedSVD(n_components=100)
feature = t_svd.fit_transform(feature)
feature = scale(feature, axis=0)
V = t_svd.components_
variance = t_svd.explained_variance_
# f_std = feature.std(axis=0)
# plt.plot(f_std)
# plt.show()
# 看LSA后各个Feature在用户间的分布
# for f in range(feature.shape[1]):
#     plt.hist(feature[:, f], 50)
#     plt.show()
# 看LSA后各个用户处feature的分布
# for u in range(feature.shape[0]):
#     plt.hist(feature[u, :], 50)
#     plt.show()
# 看各个不同topic对应域名的情况
# for idx in range(50):
#     print '%.5f' % (variance[idx]),
#     print(': ')
#     for d in np.argsort(V[idx, :])[-1:-20:-1]:
#         print pid_list[d].decode('utf-8'),
#         print '|',
#     print('...')
#     for d in np.argsort(V[idx, :])[0:21]:
#         print pid_list[d].decode('utf-8'),
#         print '|',
#     print('...')
#     plt.plot(V[idx, :])
#     plt.show()
# 看各个不同用户对应topic的情况, 及最强、最弱主题的情况
# for idx in range(feature.shape[0]):
#     print('-----------------------------')
#     max = np.argmax(feature[idx, :])
#     min = np.argmin(feature[idx, :])
#     # 最强的feature前20名域名
#     for d in np.argsort(V[max, :])[-1:-20:-1]:
#         print pid_list[d].decode('utf-8'),
#         print '|',
#     print('...')
#     # 最弱的feature前20域名
#     for d in np.argsort(V[min, :])[-1:-20:-1]:
#         print pid_list[d].decode('utf-8'),
#         print '|',
#     print('...')
#     plt.plot(feature[idx, :])
#     plt.show()
# print t_svd.explained_variance_
# print t_svd.explained_variance_ratio_
# print t_svd.explained_variance_ratio_.sum()
# plt.plot(t_svd.explained_variance_ratio_)
# plt.show()


pass


# Generate latent feature matrix
feature_style = "TFIDF_LSA"
feature_pkl_path = gen_feature_matrix(net_traffic_path=net_traffic_path, profile_path=profile_path,feature_style=feature_style)

# Clustering on latent feature matrix
K = 10
options = {'feature_style': feature_style, 'method': 'k-means++', 'K': K, 'n_init': 10}
index = do_clustering(net_traffic_path=net_traffic_path,feature_pkl_path=feature_pkl_path, options=options)

viz_profile_path = net_traffic_path+".profile/profile_(user,domain&service)-TotalBytes.pkl"
profile = cPickle.load(open(viz_profile_path, 'rb'))  # original profile vector
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