# -*-coding:utf8-*-
"""
Main script

This is the main script that glues the modules together
"""
from sklearn.cluster import KMeans
from sklearn import metrics
from emc_profile_vector import full_profile_vector
from emcdata_preprocess import data_preprocess
import numpy as np
import cPickle
import time

# Preprocess raw logs
# pkl_path = data_preprocess('CommunicationTotalByte')
pkl_path = {'userID': '../EMCdata/Dictionary/userID_set.pkl',
        'Domain': '../EMCdata/Dictionary/domain_set.pkl',
        'method': '../EMCdata/Dictionary/CommunicationTotalByte.pkl'}

# Generate profile vector
# profile_path = full_profile_vector(pkl_path=pkl_path, option='Row_Mean')
profile_path = "../EMCdata/profile_vector/profile.pkl"
profile = cPickle.load(open(profile_path, 'rb'))
numUser, featureSize = profile.shape
X = profile   # dummy assignment for future completion

# Do clustering and show performance (inertia)
max_K = 10
num_run = 5
inertia = np.zeros([max_K, num_run])
print "K, run, time, Inertia"
for idx_K, K in enumerate(np.array(range(max_K))+1):
    for run_id in range(num_run):
        t = time.time()
        model = KMeans(n_clusters=K, init='k-means++', n_init=1)   # initialize model
        model.fit(X)    # train model
        inertia[idx_K, run_id] = model.inertia_
        print "%1d, %3d, %.2f, %.6f" % (K, run_id, time.time()-t, model.inertia_)


# # Get average user profile of each cluster
# avgProfile = np.zeros([K, featureSize])
# numUserCluters = np.zeros([K])
# for u in range(numUser):
#     label = model.labels_[u]
#     avgProfile[label, :] += profile[u, :]
#     numUserCluters[label] += 1
# for k in range(K):
#     avgProfile[k, :] /= numUserCluters[k]
