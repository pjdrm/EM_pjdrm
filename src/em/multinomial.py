import math
import numpy as np

class Multinomial(object):
    def __init__(self, params):
        self._params = params

    def pmf(self, counts):
        counts = counts.astype(int)
        if not(len(counts)==len(self._params)):
            raise ValueError("Dimensionality of count vector is incorrect")
        prob = 1.
        for i,c in enumerate(counts):
            prob *= self._params[i]**counts[i]

        return prob * math.exp(self._log_multinomial_coeff(counts))

    def log_pmf(self,counts):
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
    
def em(obsMat, priorsVecs, tol=1e-6, iterations=10000):
    iteration = 0
    while iteration < iterations:
        print "Iteration %d of EM" % (iteration)
        new_priorVecs = multinomial_E_M_steps(obsMat, priorsVecs)
        priorsVecs = new_priorVecs
        iteration+=1
        '''
        delta_change = np.abs(priorsVecs[0]-new_priorVecs[0])
        if delta_change < tol:
            break
        else:
            priorsVecs = new_priorVecs
            iteration+=1
        '''
    return priorsVecs
            
def multinomial_E_M_steps(obsMat, priorsVecs):
    nPriors = len(priorsVecs)
    priorMStep = np.zeros(np.shape(priorsVecs))
    for obsVec in obsMat:
        priorUpdates = np.zeros(nPriors)
        priorNorm = 0.0
        for i, priorVec in enumerate(priorsVecs):
            pmf = pmf_obs(obsVec, priorVec)
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
        
def pmf_obs(obsVec, priorVec):
    m = Multinomial(priorVec)
    return m.pmf(obsVec)