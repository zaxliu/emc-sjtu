"""
  Generate profile vectors based on the dictionaries of uid, iid and uid & iid. The total number of users or domains can be selected.
"""

import numpy as np
import cPickle

def full_profile_vector(pkl_path, option):
    uid_list = list(cPickle.load(open(pkl_path['userID'], 'rb')))   # set cannot be indexed, so convert to list
    iid_list = list(cPickle.load(open(pkl_path['Domain'], 'rb')))
    dictionary = cPickle.load(open(pkl_path['method'], 'rb'))

    print "Generating profile vector",
    full = np.zeros((len(uid_list), len(iid_list)))
    N = len(dictionary.keys())
    n = 0
    step = 10
    for u, i in dictionary.keys():
        uid = uid_list.index(u)
        iid = iid_list.index(i)
        full[uid, iid] = dictionary[(u, i)]
        n += 1
        if int(1.0*n/N*100) == step:
            print "-%d" % (int(1.0*n/N*100)),
            step += 10
    print "Succeed"

    if option == 'Origin':
        pass
    elif option == 'Row_Percentage':
        sum_row = np.sum(full, axis=1)

        for i in range(len(uid_list)):
            if sum_row[i] != 0:
                full[i, :] = full[i, :] / sum_row[i]

    elif option == 'Row_Mean':
        mean_row = np.mean(full, axis=1)
        std_row = np.std(full, axis=1)

        for i in range(len(uid_list)):
            if std_row[i] != 0:
                full[i, :] = (full[i, :] - mean_row[i]) / std_row[i]



    f = open("../EMCdata/profile_vector/profile.pkl", 'ab')
    cPickle.dump(full, f, -1)
    return "../EMCdata/profile_vector/profile.pkl"

if __name__ == '__main__':
    full_profile_vector({'userID': '../EMCdata/Dictionary/userID_set.pkl',
            'Domain': '../EMCdata/Dictionary/domain_set.pkl',
            'method': '../EMCdata/Dictionary/CommunicationTotalByte.pkl'},'Row_Mean')



