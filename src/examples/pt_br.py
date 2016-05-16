'''
Created on 14/05/2016

@author: Mota
'''
from em.multinomial import em, Multinomial
import numpy as np
from utils.nlp import nlp_processing
from utils.rnd import make_rand_vector
from sklearn import metrics


class PT_BR_Rec(object):
    def __init__(self, inFiles):
        self.bowObs, self.docIndexes, self.vocabDic = nlp_processing(inFiles, "portuguese")
        self.vocabSize = len(self.vocabDic)
        self.nDists = len(self.docIndexes)
        self.true_labels = self.getTrueLabels(self.docIndexes)
        
    def getTrueLabels(self, docIndexes):
        label = 0
        true_labels = []
        for index in docIndexes:
            true_labels.extend([label]*index)
            label += 1
        return true_labels
           
    def cluster_obs(self):
        dists = em(self.bowObs, np.array(self.rnd_priors(self.nDists, self.vocabSize)), iterations=200, pmfType = "log")
        hyp_labels = []
        for obs in self.bowObs:
            maxProb = 0.
            label = 0
            hyp_label = 0
            for dist in dists:
                m = Multinomial(dist, "log")
                prob = m.pmf(obs)
                if prob > maxProb:
                    maxProb = prob
                    hyp_label = label
                label += 1
            hyp_labels.append(hyp_label)
        print "ARI: %f" % (metrics.adjusted_rand_score(self.true_labels, hyp_labels)) 
        
    def rnd_priors(self, nDists, vocabSize):
        priors = []
        for i in range(nDists):
            priors.append(make_rand_vector(vocabSize))
        return np.array(priors)
    
rec = PT_BR_Rec(["../../corpora/pt.txt", "../../corpora/br.txt"])
#rec.cluster_obs()