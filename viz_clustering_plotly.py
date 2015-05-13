'''
Visualize clustering results
'''

import numpy as np
import cPickle
import matplotlib.pyplot as plt
from clustering import gen_feature_matrix
from clustering import do_clustering
import plotly.plotly as py
from plotly.graph_objs import *
from sklearn.preprocessing import scale

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
num_female_c = np.zeros([K])
num_female_ratio_c = np.zeros([K])

# male & female matrix
male_index = userproperty[:, 1] == '1'
female_index = userproperty[:, 1] == '0'
male_matrix = np.zeros([num_u, num_p])
female_matrix = np.zeros([num_u, num_p])
for i in range(num_u):
    if male_index[i]:
        male_matrix[i, :] += np.ones([num_p])
    elif female_index[i]:
        female_matrix[i, :] += np.ones([num_p])

# # favorite domains splitted by gender
# profile_male = profile * male_matrix
# profile_female = profile * female_matrix
# avg_female_whole = np.mean(profile_female, axis = 0)
# avg_male_whole = np.mean(profile_male, axis = 0)
# plt.figure("Boys VS Girls")
# plt.subplot2grid((2, 1), (0, 0))
# plt.plot(range(num_p), avg_female_whole, 'r')
# plt.subplot2grid((2, 1), (1, 0))
# plt.plot(range(num_p), avg_male_whole, 'b')
# top_domains_female_whole = [pid_list[idx] for idx in avg_female_whole.argsort()[::-1][0:10]]
# print "Girls' Favorite"
# for domain in top_domains_female_whole:
#     print domain.decode('utf-8'),
#     print '|',
# print '...'
# print "Boys' Favorite"
# top_domains_male_whole = [pid_list[idx] for idx in avg_male_whole.argsort()[::-1][0:10]]
# for domain in top_domains_male_whole:
#     print domain.decode('utf-8'),
#     print '|',
# print '...'


# other properties
num_u_c_undergraduate = np.zeros([K])
num_u_c_MS = np.zeros([K])
num_u_c_PHD = np.zeros([K])
num_u_c_jiaogong = np.zeros([K])
avgAmount = np.zeros([K])

# userproperty = np.array(userproperty)
age_vector = userproperty[:, 2]
age_list = sorted(list(set(age_vector)))
print age_list
num_age = len(age_list)
disAge = np.zeros([K, num_age])
num_u_DividedByAge = np.zeros([num_age])
totalBytes_DividedByAge = np.zeros([num_age])

year_enroll_vector = userproperty[:, 3]
year_enroll = sorted(list(set(year_enroll_vector)))
print year_enroll
num_year = len(year_enroll)
disYear = np.zeros([K, num_year])

maxAmount = np.zeros([K])
medAmount = np.zeros([K])
amount = np.array([float(userproperty[u, 5]) for u in range(num_u)])

for k in range(K):
    maxAmount[k] = np.max(amount[index == k])
    amount_k = amount[index == k]
    medAmount[k] = np.median(amount_k[amount_k >= 0.0])

for u in range(num_u):
    label = index[u]
    # avgProfile[label, :] += profile[u, :]/np.max(profile[u, :])
    # totalBytes[label] += np.sum(profile[u, :])
    # num_u_c[label] += 1

    #print userproperty[u],
    #print userproperty[u][4].decode('utf-8')
    avgAmount[label] += float(userproperty[u][5])
    if userproperty[u][4] == '\xe6\x9c\xac\xe7\xa7\x91':  # undergraduate
        num_u_c_undergraduate[label] += 1
    elif userproperty[u][4] == '\xe7\xa1\x95\xe5\xa3\xab':  # MS
        num_u_c_MS[label] += 1
    elif userproperty[u][4] == '\xe5\x8d\x9a\xe5\xa3\xab':  # PHD
        num_u_c_PHD[label] += 1
    else:
        num_u_c_jiaogong[label] += 1

    num_u_DividedByAge[age_list.index(age_vector[u])] += 1
    totalBytes_DividedByAge[age_list.index(age_vector[u])] += np.sum(profile[u, :])

    disAge[label][age_list.index(age_vector[u])] += 1
    disYear[label][year_enroll.index(year_enroll_vector[u])] += 1


# Statistics of each cluster
avg_profile_whole = np.zeros([K, num_p])
avg_superposition_top = []
for k in range(K):
    # Number of users within cluster
    num_user_c[k] = np.sum(index == k)
    print k+1,
    print str(num_user_c[k])

    # Other properties
    avgAmount[k] /= (num_user_c[k] - num_u_c_jiaogong[k])
    num_u_c_undergraduate[k] /= num_user_c[k]
    num_u_c_MS[k] /= num_user_c[k]
    num_u_c_PHD[k] /= num_user_c[k]
    num_u_c_jiaogong[k] /= num_user_c[k]
    # avgProfile[k, :] /= num_user_c[k]
    disAge[k, :] /= num_user_c[k]
    disYear[k, :] /= num_user_c[k]

    # plt.figure("fig_domain")
    # plt.subplot2grid([K, 1], (k, 0), 1, 1)
    # plt.plot(np.arange(num_p), avgProfile[k, :])
    plt.figure("fig_disAge")
    plt.subplot2grid([K, 1], (k, 0), 1, 1)
    plt.plot(age_list, disAge[k, :])
    # plt.ylim([0, 1])
    plt.figure("fig_disYear_enrollment")
    plt.subplot2grid([K, 1], (k, 0), 1, 1)
    plt.plot(year_enroll, disYear[k, :])

    # Average profile within cluster
    profile_k = profile[index == k, :]  # select the profile of users within this cluster
    profile2_k = profile2[index == k, :]

    profile_male_k = profile[index == k, :] * male_matrix[index == k, :] # select the profile of users within this cluster
    profile2_male_k = profile2[index == k, :] * male_matrix[index == k, :]
    profile_female_k = profile[index == k, :] * female_matrix[index == k, :]  # select the profile of users within this cluster
    profile2_female_k = profile2[index == k, :] * female_matrix[index == k, :]

    avg_profile = np.mean(profile_k, axis=0)
    avg_profile_whole[k, :] = avg_profile
    avg_profile2 = np.mean(profile2_k, axis=0)

    avg_male_profile = np.mean(profile_male_k, axis=0)
    avg_male_profile2 = np.mean(profile2_male_k, axis=0)
    avg_female_profile = np.mean(profile_female_k, axis=0)
    avg_female_profile2 = np.mean(profile2_female_k, axis=0)

    plt.figure('Average Profile')
    plt.subplot2grid([K, 1], (k, 0), 1, 1)
    plt.plot(np.arange(num_p), avg_profile)

    # List top domain names with in cluster
    top_domains = [pid_list[idx] for idx in avg_profile.argsort()[::-1][0:10]]
    for idx in avg_profile.argsort()[::-1][0:8]:
        avg_superposition_top.append(idx)
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

    # List top domain names with in cluster (male)
    top_domains_male = [pid_list[idx] for idx in avg_male_profile.argsort()[::-1][0:10]]
    for domain in top_domains_male:
        print domain.decode('utf-8'),
        print '|',
    print '...'
    top_domains2_male = [pid_list[idx] for idx in avg_male_profile2.argsort()[::-1][0:10]]
    for domain in top_domains2_male:
        print domain.decode('utf-8'),
        print '|',
    print '...'
    print '---------------------------'
    # List top domain names with in cluster (female)
    top_domains_female = [pid_list[idx] for idx in avg_female_profile.argsort()[::-1][0:10]]
    for domain in top_domains_female:
        print domain.decode('utf-8'),
        print '|',
    print '...'
    top_domains2_female = [pid_list[idx] for idx in avg_female_profile2.argsort()[::-1][0:10]]
    for domain in top_domains2_female:
        print domain.decode('utf-8'),
        print '|',
    print '...'
    print '---------------------------'

    # Gender statistics
    num_man_c[k] = np.sum(userproperty[index == k, 1]=='1')
    num_man_ratio_c[k] = num_man_c[k]/num_user_c[k]


# Show heatmap with plotly
avg_superposition_top = list(set(avg_superposition_top))
# avg_profile_whole = scale(avg_profile_whole, axis=1, with_mean=True)
for i in range(K):
    avg_profile_whole[i, :] /= np.max(avg_profile_whole[i, :])

data = Data([
    Heatmap(
        x=[pid_list[idx] for idx in avg_superposition_top],
        z=avg_profile_whole[:, avg_superposition_top]
    )
])
plot_url = py.plot(data, filename='basic-heatmap')

# Other properties
plt.figure("fig_amount")
plt.plot(range(K), avgAmount)
plt.plot(range(K), maxAmount)
plt.plot(range(K), medAmount)
plt.figure("fig_undergraduate")
plt.plot(range(K), num_u_c_undergraduate)
# plt.figure("fig_MS")
plt.plot(range(K), num_u_c_MS)
# plt.figure("fig_PHD")
plt.plot(range(K), num_u_c_PHD)
# plt.figure("fig_jiaogong")
plt.plot(range(K), num_u_c_jiaogong)
plt.ylim([0, 1])

# Draw gender contrast figure
plt.figure('Gender distribution')
plt.bar(np.arange(K), num_man_ratio_c)
overall_man_ratio = np.sum(num_man_c)/num_u
print 'Overall ratio of male: %.1f %%' % (overall_man_ratio*100)
plt.ylim([0.5, 0.8])

plt.show()
pass