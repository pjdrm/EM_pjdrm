'''
Created on 14/05/2016

@author: Mota
'''
from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords

def nlp_processing(inFiles, lang):
    fileIndexes = []
    obs = []
    for inFilPath in inFiles:
        with open(inFilPath) as f:
            lines = [unicode(lin, errors='replace') for lin in f.readlines()]
        fileIndexes.append(len(lines))
        obs += lines
    vectorizer = CountVectorizer(analyzer = "word", strip_accents = "unicode", stop_words = stopwords.words(lang))
    bowObsMatrix = vectorizer.fit_transform(obs).toarray()
    return bowObsMatrix, fileIndexes, vectorizer.vocabulary_