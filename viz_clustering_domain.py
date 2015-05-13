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

# =========== Load supplementary variable ==========
pid_list = list(cPickle.load(open(pid_path, 'rb')))

# =========== Generate latent feature matrix ============
feature_style = "TFIDF_Trans"
print 'Generate feature from raw profile using '+ feature_style
feature_pkl_path = gen_feature_matrix(net_traffic_path=net_traffic_path,
                                      profile_path=profile_path,
                                      feature_style=feature_style)

# =========== Clustering on latent feature matrix ===========
K = 12
options = {'feature_style': feature_style, 'method': 'k-means++', 'K': K, 'n_init': 10}
print 'Doing user clustering with method: ' + options['method'] + ' (K = ' + str(K) + ')'
index = do_clustering(net_traffic_path=net_traffic_path,
                      feature_pkl_path=feature_pkl_path,
                      options=options)

# =========== Visualization ===========
# Initialization
print 'Visualizing matrix from: ' + viz_profile_path
profile = cPickle.load(open(viz_profile_path, 'rb'))  # original profile vector
num_u, num_p = profile.shape

# Temp variables
num_domain_c = np.zeros([K])

# Statistics of each cluster
for k in range(K):
    # List top domain names within cluster
    domains = []
    for idx in range(num_p):
        if index[idx] == k:
            domains.append(pid_list[idx].decode('utf-8'))

    # profile
    profile_k = np.sum(profile[:, index==k], axis=0)

    # Number of domains within cluster
    num_domain_c[k] = np.sum(index == k)
    print k+1,
    print str(num_domain_c[k])


    for idx in np.argsort(profile_k)[::-1]:
        print domains[idx],
    print '---------------------------'


# Draw gender contrast figure
plt.show()
