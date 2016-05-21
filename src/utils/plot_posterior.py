'''
Created on May 21, 2016

@author: pjdrm
'''
import operator
import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np

def plotPosterior(posteriors, labelDic, n, colors):
    f, axarr = plt.subplots(len(posteriors))
    xAxis = [x/10. for x in range(0, 11)]
    for posterior, ax_i, color in zip(posteriors, range(len(posteriors)), colors):
        labelsVals = {}
        for i, val in enumerate(posterior):
            labelsVals[labelDic[i]] = val
        sorted_dic = sorted(labelsVals.items(), key=operator.itemgetter(1))
        yLabels = [label for label, val in sorted_dic[:n]]
        y_pos = np.arange(len(yLabels))/3.
        axarr[ax_i].barh(y_pos, [labelsVals[y] for y in yLabels], align='center', color=color, height=0.2)
        axarr[ax_i].set_yticks(y_pos)
        axarr[ax_i].set_yticklabels(yLabels)

    plt.xlabel('Probability')
    plt.show()

'''
aPost = [0.2, 0.5, 0.6, 0.1, 0.8]
aDic = {0: "A", 1:"B", 2:"C", 3:"D", 4:"E"}
plotPosterior([aPost, aPost], [aDic, aDic], 5, ['r', 'b'])
'''