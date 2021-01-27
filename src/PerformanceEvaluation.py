from copy import deepcopy
from math import inf
import sys

from Util import *

MatrixSizes = [10]
similarityLow = [0.001,0.01,0.1]
similarityHigh = [0.8]
similarityThreshHolds = [0.7, 0.8, 0.9]

random.seed(0)
sampleSize = 1000

if __name__ == "__main__":
    # load, and process the smalldataset
    data = load_dataset_from_csv("dataset/news_articles_small.csv")
    make_shingles(data)
    hash_shingles(data)
    sampleDocumentList = [random.randrange(0, len(data) - 1) for i in range(sampleSize)]
    for k in MatrixSizes:  # experiment with different k
        for low in similarityLow:
            for high in similarityHigh:
                if (low >= high): continue
                hashfuncs = hash_funcs(k)
                minhash_shingles(data, hashfuncs)
                buckets = LSH(data, low, high)

                precision = dict()
                correctResults = dict()
                for si in similarityThreshHolds:
                    precision[si] = 0
                    correctResults[si] = 0


                for s in sampleDocumentList:  # try to randomly sample 10 plagiarized articles
                    sampleArticle = data[s]  # take a random article from collection
                    originalArticle = sampleArticle
                    sampleArticle = NewsArticle(sampleArticle.ID, sampleArticle.content)
                    make_shingles([sampleArticle])
                    hash_shingles([sampleArticle])
                    # change 5% of the shingles --> results in 95/105=90.5% similarity on jaccard index
                    for c in range(int(len(sampleArticle.shingles) / 20)):
                        sampleArticle.shingles[random.randrange(0, len(sampleArticle.shingles) - 1)] = \
                            random.randrange(-2 ** 64, 2 ** 64)
                    minhash_shingles([sampleArticle], hashfuncs)  # minhash the sample article
                    queryHash = LSH([sampleArticle], low, high)  # hash the sample article
                    candidates = set()
                    for key in queryHash.keys():
                        candidates.update(buckets.get(key, []))

                    correct = dict()
                    for si in similarityThreshHolds:
                        correct[si] = 0
                    for r in candidates:
                        if r == sampleArticle.ID:
                            for si in similarityThreshHolds:
                                correct[si] += 1
                            continue
                        candidateDoc = data[int(r)]
                        jaccard = Jaccard_sim(candidateDoc.shingles, sampleArticle.shingles)
                        for si in similarityThreshHolds:
                            if (jaccard > si):
                                correct[si] += 1
                    for si in similarityThreshHolds:
                        precision[si] += correct[si] / len(candidates) if len(candidates) != 0 else 1
                        correctResults[si] += correct[si]

                print("M={},s_low={},s_high={}:".format(k, low, high))
                for si in similarityThreshHolds:
                    precision[si] /= sampleSize
                    print(
                        "Precision@{}={},Recall-Score@{}={}, ".format(si, precision[si], si, correctResults[si]))
                print()
                # print("found candidates={} for randomized sample={}, with M={},s_low={},s_high={}".format(candidates,sampleArticle.ID,k, low,high))
