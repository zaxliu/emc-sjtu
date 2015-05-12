# -*-encoding:utf:8-*-
'''
Visualize statistics of raw profile and other intermediate matrixs
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

# ========== Define file paths =====================
net_traffic_path = "../EMCdata/net_traffic.dat"
profile_path = net_traffic_path+".profile/profile_(user,domain)-TotalBytes.pkl"
# profile_path = net_traffic_path+".profile/profile_(user,domain)-VisitingNum.pkl"
# profile_path = net_traffic_path+".profile/profile_(user,domain)-Duration.pkl"
# profile_path = net_traffic_path+".profile/profile_(user,domain)-RequestNum.pkl"
pid_path = net_traffic_path+".profile/pid_(user,domain).pkl"  # Column ID of raw profile matrix

# ========== Load supplementary variable ==========
pid_list = list(cPickle.load(open(pid_path, 'rb')))

# ========== Statistics of raw profile ============
profile_matrix = cPickle.load(open(profile_path, 'rb'))
# col_mean = profile_matrix.mean(axis=0)
# col_med = np.median(profile_matrix, axis=0)
# row_mean = profile_matrix.mean(axis=1)
# row_med = np.median(profile_matrix, axis=1)
# # 查看stop-domain的情况
# for i, idx in enumerate(np.argsort(col_med)[-1:-100:-1]):    # 依column median中倒序查看domain
#     # plt.hist(np.log10(1+np.sort(profile_matrix[:, idx])[::-1]))    # 查看用户访问该domain的分布情况
#     print i,                                                      # median排序序号
#     print col_med[idx],
#     print np.sum(profile_matrix[:, idx]==0.0),                    # 没有访问该网站的用户数
#     print pid_list[idx].decode('utf-8')                          # domain 名称
#     # plt.show()

# ========== Statistics of tf-idf ===================
# profile_matrix = np.log10(1+profile_matrix)
ti_trans = TfidfTransformer(use_idf=True, smooth_idf=True, sublinear_tf=True, norm='l2')
feature = ti_trans.fit_transform(profile_matrix).toarray()
# 随机查看用户tfidf值最大的几个域名
# for u in np.random.random_integers(0, feature.shape[0], 20)[0:10]:
#     domain_order = np.argsort(feature[u, :])[-1:-20:-1]
#     for d in domain_order:
#         print pid_list[d].decode('utf-8'),
#     print('...')
#     plt.plot(feature[u, :])
#     plt.show()
# 查看各个域名的tfidf在不同用户间取值的分布
# median = np.median(feature, axis=0)
# for f in np.argsort(median)[::-1]:
#     print f,
#     print pid_list[f].decode('utf-8'),
#     feature_sub = feature[:, f]
#     plt.boxplot(feature_sub)
#     plt.ylim([-.5, 1])
#     plt.show()
#     pass
# print '...'

# ========== Statistics of LSA ======================
n_comp = 200
t_svd = TruncatedSVD(n_components=n_comp)
feature = t_svd.fit_transform(feature)
feature = scale(feature, axis=0)
V = t_svd.components_
print t_svd.explained_variance_ratio_.sum()
# plt.plot(t_svd.explained_variance_ratio_)
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
# variance = t_svd.explained_variance_
# for idx in range(n_comp):
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
