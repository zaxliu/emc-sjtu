# -*-coding:utf8-*-
"""

"""
from sklearn.cluster import KMeans
import numpy as np

# Load data
profile = np.zeros([1000, 100])
featureSize = 100
numUser = 1000
# Preprocess to form input
X = 0   # dummy assignment for future completion

# Do clustering
K = 10  # define number of clusters
model = KMeans(n_clusters=K, init='k-means++', n_init=10)   # initialize model
model.fit(X)    # train model

# Get average user profile of each cluster
avgProfile = np.zeros([K, featureSize])
numUserCluters = np.zeros([K])
for u in range(numUser):
    label = model.labels_[u]
    avgProfile[label, :] += profile[u, :]
    numUserCluters[label] += 1
for k in range(K):
    avgProfile[k, :] /= numUserCluters[k]
