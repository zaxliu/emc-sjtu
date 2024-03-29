# -*-coding:utf8-*-
import os
import time
import cPickle
import numpy as np
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.preprocessing import Normalizer
from sklearn.preprocessing import normalize
from sklearn.preprocessing import scale
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def gen_feature_matrix(net_traffic_path, profile_path, feature_style):
    profile = cPickle.load(open(profile_path, 'rb'))  # original profile vector
    feature = np.zeros(profile.shape)

    if feature_style == 'same':
        feature = profile
        pass
    elif feature_style == 'RowNorm':
        sum_row = np.sum(profile, axis=1)
        mean_row = np.mean(profile, axis=1)
        std_row = np.std(profile, axis=1)
        for i in range(profile.shape[0]):
            if sum_row[i] != 0:
                feature[i, :] = feature[i, :] / sum_row[i]  # Normalize profile rows so that sum to one
                # feature[i, :] = (profile[i, :] - mean_row[i]) / std_row[i]  # Standardize profile rows so that mean=0, std=1
    elif feature_style == 'TFIDF':      # TFIDF
        # us tf=1+log(tf), set sublinear_tf=True
        # want to cancel row_std=1, set norm=None
        ti_trans = TfidfTransformer(use_idf=True, sublinear_tf=True, norm='l2')
        feature = ti_trans.fit_transform(profile).toarray()
        feature = scale(feature, axis=0)
        feature = scale(feature, axis=1)
    elif feature_style == 'TFIDF_LSA':  # TFIDF followed by LSA dimentionality reduction
        # us tf=1+log(tf), set sublinear_tf=True    (dispersed variance)
        # want to cancel row_std=1, set norm=None
        tf_idf = TfidfTransformer(use_idf=True, sublinear_tf=True, norm='l2')
        feature = tf_idf.fit_transform(profile)
        t_svd = TruncatedSVD(n_components=80)
        feature = t_svd.fit_transform(feature)
        print 'Total explained variance: ',
        print t_svd.explained_variance_ratio_.sum()
        feature = scale(feature, axis=0)
        feature = scale(feature, axis=1)
    elif feature_style == 'TFIDF_Trans':
        tf_idf = TfidfTransformer(use_idf=True, sublinear_tf=True, norm='l2')
        feature = tf_idf.fit_transform(profile.transpose()).toarray()
        feature = scale(feature, axis=0)
        feature = scale(feature, axis=1)
    elif feature_style == 'TFIDF_LSA_Trans':
        tf_idf = TfidfTransformer(use_idf=True, sublinear_tf=True, norm='l2')
        feature = tf_idf.fit_transform(profile.transpose())
        t_svd = TruncatedSVD(n_components=80)
        feature = t_svd.fit_transform(feature)
        print 'Total explained variance: ',
        print t_svd.explained_variance_ratio_.sum()
        feature = scale(feature, axis=0)
        feature = scale(feature, axis=1)
    else:
        print 'Unknown feature style!'
    feature_path = net_traffic_path+".feature/"
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
    # elif method == 'lsa-k-means++':


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
        model = KMeans(n_clusters=K, init=method, n_init=n_init, verbose=False)   # initialize model
        model.fit(feature)    # train model
        index_pkl_path = index_path+'index_feature='+feature_style+'_method=k-means++_K='+str(K)+'_n_init='+str(n_init)+'.pkl'

    f = open(index_pkl_path, 'wb')
    return model.labels_
    # return index_pkl_path


if __name__ == '__main__':
    net_traffic_path = "../EMCdata/net_traffic.dat"
    profile_path = "../EMCdata/net_traffic.dat.profile/profile_(user,domain)-TotalBytes.pkl"
    feature_style = "TFIDF_LSA"
    feature_pkl_path = gen_feature_matrix(net_traffic_path=net_traffic_path, profile_path=profile_path,feature_style=feature_style)
    #
    sweep_options = {'method': 'k-means++', 'K_range': range(1, 20), 'num_run': 1, 'n_init': 10}
    do_clustering_sweep(feature_pkl_path=feature_pkl_path, sweep_options=sweep_options)
    # K = 7
    # options = {'feature_style': feature_style, 'method': 'k-means++', 'K': K, 'n_init': 10}
    # index = do_clustering(net_traffic_path=net_traffic_path,feature_pkl_path=feature_pkl_path, options=options)
    #
    # feature = cPickle.load(open(feature_pkl_path, 'rb'))
    # num_u, num_f = feature.shape
    # avg_feature = np.zeros([K, num_f])
    # num_u_c = np.zeros([K])
    #
    # for u in range(num_u):
    #     label = index[u]
    #     avg_feature[label, :] += feature[u, :]
    #     num_u_c[label] += 1
    #
    # for k in range(K):
    #     plt.subplot2grid([K, 1], (k, 0), 1, 1)
    #     plt.plot(np.arange(num_f), avg_feature[k, :])
    # plt.show()





