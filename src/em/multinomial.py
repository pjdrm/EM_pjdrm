import math
import numpy as np
import matplotlib.pyplot as plt

class Multinomial(object):
    def __init__(self, params, pmfType = "reg"):
        self._params = params
        self.pmfType = pmfType
    
    def pmf(self, counts):
        if self.pmfType == "reg":
            return self.reg_pmf(counts)
        elif self.pmfType == "log":
            return self.log_pmf(counts)
        
    def reg_pmf(self, counts):
        counts = counts.astype(int)
        if not(len(counts)==len(self._params)):
            raise ValueError("Dimensionality of count vector is incorrect")
        prob = 1.
        for i,c in enumerate(counts):
            prob *= self._params[i]**counts[i]
        
        return prob * math.exp(self._log_multinomial_coeff(counts))

    def log_pmf(self,counts):
        counts = counts.astype(int)
        if not(len(counts)==len(self._params)):
            raise ValueError("Dimensionality of count vector is incorrect")
        prob = 0.
        for i,c in enumerate(counts):
            prob += counts[i]*math.log(self._params[i])
        return prob + self._log_multinomial_coeff(counts)

    def _log_multinomial_coeff(self, counts):
        return self._log_factorial(sum(counts)) - sum(self._log_factorial(c) for c in counts)

    def _log_factorial(self, num):
        if not round(num)==num and num > 0:
            raise ValueError("Can only compute the factorial of positive ints")
        return sum(math.log(n) for n in range(1,num+1))
    
def em(obsMat, priorsVecs, tol=1e-6, iterations=10000, pmfType = "reg"):
    iteration = 0
    priorLen = float(len(priorsVecs[0]))
    delta_change_arr = []
    while iteration < iterations:
        #print "Iteration %d of EM" % (iteration)
        new_priorVecs = multinomial_E_M_steps(obsMat, priorsVecs, pmfType)
        delta_change = np.sum(np.abs(priorsVecs[0]-new_priorVecs[0]))/priorLen
        print "Iteration %d of EM Prior convergence: %f" % (iteration, delta_change)
        delta_change_arr.append(delta_change)
        priorsVecs = new_priorVecs
        iteration+=1
        if delta_change < tol:
            break
        else:
            priorsVecs = new_priorVecs
            iteration+=1
    plt.plot(range(len(delta_change_arr)), delta_change_arr, 'ro')
    plt.savefig('../../prior_conv.png')
    plt.close()
    return priorsVecs
            
def multinomial_E_M_steps(obsMat, priorsVecs, pmfType = "reg"):
    nPriors = len(priorsVecs)
    priorMStep = np.zeros(np.shape(priorsVecs))
    for obsVec in obsMat:
        priorUpdates = np.zeros(nPriors)
        priorNorm = 0.0
        for i, priorVec in enumerate(priorsVecs):
            pmf = pmf_obs(obsVec, priorVec, pmfType)
            priorUpdates[i] = pmf
            priorNorm += pmf
        priorUpdates = priorUpdates / priorNorm
        for i, priorUp in enumerate(priorUpdates):
            priorUpWeightedCounts = obsVec*priorUp
            priorMStep[i] = priorMStep[i] + priorUpWeightedCounts
    return normalizeMatrix(priorMStep)
        
def normalizeMatrix(mat):
    for i in range(len(mat)):
        n = np.sum(mat[i])
        mat[i] = mat[i] / n
    return mat
        
def pmf_obs(obsVec, priorVec, pmfType = "reg"):
    m = Multinomial(priorVec, pmfType)
    return m.pmf(obsVec)