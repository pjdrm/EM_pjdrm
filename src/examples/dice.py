'''
Created on 13/05/2016

@author: Mota
'''
import numpy as np
from em.multinomial import em

def diceThrow(n, pVals):
    return np.random.multinomial(n, pVals)

def runDiceExample(thetaA, thetaB, nExperiments, nThrows, thetaAPrior, thetaBPrior):
    nFaces = len(thetaA)
    thetaA_obs = np.zeros((nExperiments, nFaces))
    thetaB_obs = np.zeros((nExperiments, nFaces))
    for i in range(nExperiments):
        thetaA_obs[i] = diceThrow(nThrows, thetaA)
        
    for i in range(nExperiments):
        thetaB_obs[i] = diceThrow(nThrows, thetaB)
     
    
    obs = np.vstack((thetaA_obs, thetaB_obs))
    dists = em(obs, np.array([thetaAPrior, thetaBPrior]), iterations=1000)
    print dists
    
thetaA = [0.2, 0.2, 0.2, 0.1, 0.1, 0.2]
thetaB = [0.5, 0.1, 0.1, 0.1, 0.1, 0.1]
nExperiments = 2000
nThrows = 10

thetaAPrior = [0.1, 0.3, 0.1, 0.1, 0.1, 0.3]
thetaBPrior = [0.3, 0.1, 0.3, 0.1, 0.1, 0.1]
runDiceExample(thetaA, thetaB, nExperiments, nThrows, thetaAPrior, thetaBPrior)