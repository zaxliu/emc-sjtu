# -*-coding:utf8-*-
import os
import time
import cPickle
import json
import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def gen_feature_matrix(net_traffic_path, profile_path, feature_style):
    profile = cPickle.load(open(profile_path, 'rb'))  # original profile vector
    feature = np.zeros(profile.shape)
    feature_path = net_traffic_path+".feature/"

    if feature_style == 'Original':
        feature = profile
        pass
    elif feature_style == 'Row_Percentage':
        sum_row = np.sum(profile, axis=1)
        for i in range(profile.shape[0]):
            if sum_row[i] != 0:
                feature[i, :] = feature[i, :] / sum_row[i]
    elif feature_style == 'Row_Normalize':
        mean_row = np.mean(profile, axis=1)
        std_row = np.std(profile, axis=1)
        for i in range(profile.shape[0]):
            if std_row[i] != 0:
                feature[i, :] = (profile[i, :] - mean_row[i]) / std_row[i]

    if not os.path.exists(feature_path):
        os.mkdir(feature_path)
    feature_pkl_path = feature_path+"feature_"+feature_style+".pkl"
    f = open(feature_pkl_path, 'wb')
    cPickle.dump(feature, f, -1)
    f.close()
    return feature_pkl_path


def do_clustering_sweep(feature_pkl_path, sweep_options):
    method = sweep_options['method']
    feature = cPickle.load(open(feature_pkl_path, 'rb'))
    # Do clustering using specified method and sweep parameters
    if method == 'k-means++':
        K_range = sweep_options['K_range']
        num_run = sweep_options['num_run']
        n_init = sweep_options['n_init']
        inertia = np.zeros([len(K_range), num_run])
        print "     K,    run,   time,    Inertia"
        for idx_K, K in enumerate(K_range):
            for run_id in range(num_run):
                t = time.time()
                model = KMeans(n_clusters=K, init=method, n_init=n_init)   # initialize model
                model.fit(feature)    # train model
                inertia[idx_K, run_id] = model.inertia_
                print "%6d, %6d, %6.2f, %10.6f" % (K, run_id, time.time()-t, model.inertia_)
        plt.plot(K_range, inertia.mean(axis=1))
        plt.show()


def do_clustering(net_traffic_path, feature_pkl_path, options):
    method = options['method']
    feature_style = options['feature_style']
    feature = cPickle.load(open(feature_pkl_path, 'rb'))
    index_path = net_traffic_path+".index/"
    if not os.path.exists(index_path):
        os.mkdir(index_path)
    if method == 'k-means++':
        K = options['K']
        n_init = options['n_init']
        model = KMeans(n_clusters=K, init=method, n_init=n_init, verbose=True)   # initialize model
        model.fit(feature)    # train model
        index_pkl_path = index_path+'index_feature='+feature_style+'_method=k-means++_K='+str(K)+'_n_init='+str(n_init)+'.pkl'
    f = open(index_pkl_path, 'wb')
    return model.labels_
    # return index_pkl_path


if __name__ == '__main__':
    net_traffic_path = "../EMCdata/net_traffic.dat"
    profile_path = "../EMCdata/net_traffic.dat.profile_vector/profile.pkl"
    feature_style = "Row_Normalize"
    feature_pkl_path = gen_feature_matrix(net_traffic_path=net_traffic_path,
                                          profile_path=profile_path,
                                          feature_style=feature_style)

    # sweep_options = {'method': 'k-means++', 'K_range': range(1, 20), 'num_run': 1, 'n_init': 1}
    # do_clustering_sweep(feature_pkl_path=feature_pkl_path, sweep_options=sweep_options)
    options = {'feature_style': feature_style, 'method': 'k-means++', 'K': 7, 'n_init': 1}
    do_clustering(net_traffic_path=net_traffic_path,
                  feature_pkl_path=feature_pkl_path,
                  options=options)





