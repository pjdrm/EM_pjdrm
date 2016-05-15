'''
Created on 14/05/2016

@author: Mota
'''
from random import randint
import numpy as np

def make_rand_vector(dim):
    vec = [randint(1, dim / 2 + 1) for i in range(dim)]
    vec_np = np.array(vec)
    norm = np.sum(vec_np)*1.
    return vec_np / norm
