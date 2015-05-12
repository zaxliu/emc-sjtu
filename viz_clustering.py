'''
Visualize clustering results
'''

import numpy as np
import cPickle
import matplotlib.pyplot as plt
from clustering import gen_feature_matrix
from clustering import do_clustering


# ========== Define file paths ==============
net_traffic_path = "../EMCdata/net_traffic.dat"
profile_path = net_traffic_path+".profile/profile_(user,domain)-TotalBytes.pkl"        # Profile used for clustering
# profile_path = net_traffic_path+".profile/profile_(user,domain)-VisitingNum.pkl"
# profile_path = net_traffic_path+".profile/profile_(user,domain)-Duration.pkl"
# profile_path = net_traffic_path+".profile/profile_(user,domain)-RequestNum.pkl"
pid_path = net_traffic_path+".profile/pid_(user,domain).pkl"                             # Column ID of raw profile
viz_userproperty_path = "../EMCdata/net_users.dat.userproperty/user_property.pkl"
viz_feature_style = "TFIDF"
viz_profile_path = gen_feature_matrix(net_traffic_path=net_traffic_path,                     # Visualization matrix #1
                                      profile_path=profile_path,
                                      feature_style=viz_feature_style)
viz_profile_path2 = net_traffic_path+".profile/profile_(user,domain)-TotalBytes.pkl"   # Visualization matrix #2
# viz_profile_path2 = net_traffic_path+".profile/profile_(user,domain)-VisitingNum.pkl"
# viz_profile_path2 = net_traffic_path+".profile/profile_(user,domain)-Duration.pkl"
# viz_profile_path2 = net_traffic_path+".profile/profile_(user,domain)-RequestNum.pkl"

# =========== Load supplementary variable ==========
pid_list = list(cPickle.load(open(pid_path, 'rb')))

# =========== Generate latent feature matrix ============
feature_style = "TFIDF_LSA"
print 'Generate feature from raw profile using '+ feature_style
feature_pkl_path = gen_feature_matrix(net_traffic_path=net_traffic_path,
                                      profile_path=profile_path,
                                      feature_style=feature_style)

# =========== Clustering on latent feature matrix ===========
K = 8
options = {'feature_style': feature_style, 'method': 'k-means++', 'K': K, 'n_init': 10}
print 'Doing user clustering with method: ' + options['method'] + ' (K = ' + str(K) + ')'
index = do_clustering(net_traffic_path=net_traffic_path,
                      feature_pkl_path=feature_pkl_path,
                      options=options)

# =========== Visualization ===========
# Initialization
print 'Visualizing matrix from: ' + viz_profile_path
profile = cPickle.load(open(viz_profile_path, 'rb'))  # original profile vector
profile2 = cPickle.load(open(viz_profile_path2, 'rb'))
num_u, num_p = profile.shape
userproperty = np.array(cPickle.load(open(viz_userproperty_path, 'rb')))  # user_property_matrix, 0 for F, 1 for M.

# Temp variables
num_user_c = np.zeros([K])
num_man_c = np.zeros([K])
num_man_ratio_c = np.zeros([K])

# Statistics of each cluster
for k in range(K):
    # Number of users within cluster
    num_user_c[k] = np.sum(index == k)
    print k+1,
    print str(num_user_c[k])

    # Average profile within cluster
    profile_k = profile[index == k, :]  # select the profile of users within this cluster
    profile2_k = profile2[index == k, :]
    avg_profile = np.mean(profile_k, axis=0)
    avg_profile2 = np.mean(profile2_k, axis=0)
    plt.figure('Average Profile')
    plt.subplot2grid([K, 1], (k, 0), 1, 1)
    plt.plot(np.arange(num_p), avg_profile)

    # List top domain names with in cluster
    top_domains = [pid_list[idx] for idx in avg_profile.argsort()[::-1][0:10]]
    for domain in top_domains:
        print domain.decode('utf-8'),
        print '|',
    print '...'
    top_domains2 = [pid_list[idx] for idx in avg_profile2.argsort()[::-1][0:10]]
    for domain in top_domains2:
        print domain.decode('utf-8'),
        print '|',
    print '...'
    print '---------------------------'

    # Gender statistics
    num_man_c[k] = np.sum(userproperty[index == k, 1]=='1')
    num_man_ratio_c[k] = num_man_c[k]/num_user_c[k]

# Draw gender contrast figure
plt.figure('Gender distribution')
plt.bar(np.arange(K), num_man_ratio_c)
overall_man_ratio = np.sum(num_man_c)/num_u
print 'Overall ratio of male: %.1f %%' % (overall_man_ratio*100)
plt.ylim([0.5, 0.8])

plt.show()
