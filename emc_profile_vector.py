"""
  Generate profile vectors based on the dictionaries of uid, iid and uid & iid. The total number of users or domains can be selected.
"""

#from __future__ import division
import numpy as np


def full_profile_vector(uid_list, iid_list, dictionary):
    full = np.zeros((len(uid_list), len(iid_list)))

    for item in dictionary.keys():
        uid = uid_list.index(item[0])
        iid = iid_list.index(item[1])
        full[uid, iid] = dictionary[item]

    return full

def full_profile_vector_norm(uid_list, iid_list, dictionary):
    full = full_profile_vector(uid_list, iid_list, dictionary)
    full_norm = full.copy()

    sum_row = full.sum(axis=1)

    for i in range(len(uid_list)):
        if sum_row[i] != 0:
            full_norm[i, :] = full_norm[i, :] / sum_row[i]

    return full_norm



uid_list = [1, 2, 3, 4]
iid_list = ['baidu', 'qq']
dictionary = {(1, 'baidu'): 5, (4, 'qq'): 10, (1,'qq'): 18}
full = full_profile_vector_norm(uid_list, iid_list, dictionary)
print full



