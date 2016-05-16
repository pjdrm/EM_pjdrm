'''
Created on 14/05/2016

@author: Mota
'''
from os import listdir
from newspaper import Article
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer


cachDir = "../../cache"
urlFilters = [".shtml"]
txtFilter = ["Not Found", "o site da RFI precisa que o JavaScript", "telefone de onde ligou", "encontrada Um link de favoritos/bookmark desatualizado", "ter sido removida, estar temporariamente"]

def nlp_processing(inFiles, lang):
    fileIndexes = []
    obs = []
    for inFilPath in inFiles:
        lines = scrapeURLS(inFilPath)
        fileIndexes.append(len(lines))
        obs += lines
    vectorizer = CountVectorizer(analyzer = "word", strip_accents = "unicode", stop_words = stopwords.words(lang))
    bowObsMatrix = vectorizer.fit_transform(obs).toarray()
    return bowObsMatrix, fileIndexes, vectorizer.vocabulary_

def scrapeURLS(inFilPath):
    texts = []
    cache = loadCache()
    toDelURLs = []
    with open(inFilPath) as f:
        urls = f.readlines()
    for url in urls:
        if filter(urlFilters, url):
            toDelURLs.append(url)
            
        if url in cache:
            txt = cache[url]
        else:
            print "Scraping URL %s" % url
            article = Article(url)
            article.download()
            article.parse()
            txt = article.text.replace("\n", " ").replace("  ", " ").strip()
            if txt == "" or filter(txtFilter, txt):
                toDelURLs.append(url)
                continue
            cacheURL(url, txt)
        texts.append(txt)
        deleteURLs(inFilPath, toDelURLs)
    return texts

def loadCache():
    urlFiles = listdir(cachDir)
    cache = {}
    for filePath in urlFiles:
        with open(cachDir + "/" + filePath) as f:
            lins = f.readlines()
            cache[lins[0]] = lins[1]
    return cache

def cacheURL(url, txt):
    urlFiles = listdir(cachDir)
    if len(urlFiles) == 0:
        newIndex = 0
    else:
        newIndex = max([int(x.replace(".txt", "")) for x in urlFiles]) + 1
    with open(cachDir + "/" + str(newIndex) + ".txt", "w+") as outFile:
        s = url.strip() + "\n" + txt
        outFile.write(s.encode("UTF-8"))
        
def deleteURLs(inFilPath, toDelURLs):
    with open(inFilPath) as f:
        lins = f.readlines()
    filteredURLs = list(set(lins) - set(toDelURLs))
    
    with open(inFilPath, "w") as outFile:
        outFile.writelines(filteredURLs)
        
def filter(filters, txt):
    for filter_exp in filters:
        if filter_exp in txt:
            return True
    return False
    