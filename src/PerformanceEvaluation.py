from copy import deepcopy
from math import inf
import sys

from Util import *

MatrixSizes = [20, 50, 100, 200]
similarityLow = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8]
similarityHigh = [0.7, 0.8, 0.9]

random.seed(0)

if __name__ == "__main__":
    # load, and process the smalldataset
    data = load_dataset_from_csv("dataset/news_articles_small.csv")
    make_shingles(data)
    hash_shingles(data)
    for k in MatrixSizes:  # experiment with different k
        for low in similarityLow:
            for high in similarityHigh:
                if (low >= high): continue
                hashfuncs=hash_funcs(k)
                minhash_shingles(data, hashfuncs)
                buckets = LSH(data, low, high)
                foundArticle = 0
                for i in range(10):  # try to randomly sample 10 plagiarized articles

                    sampleArticle = data[random.randrange(0, len(data) - 1)]  # take a random article from collection
                    originalArticle =sampleArticle
                    sampleArticle = NewsArticle(sampleArticle.ID,sampleArticle.content)
                    make_shingles([sampleArticle])
                    hash_shingles([sampleArticle])
                    # change 5% of the shingles --> results in 95/105=90.5% similarity on jaccard index
                    for c in range(int(len(sampleArticle.shingles)/20)):
                        sampleArticle.shingles[random.randrange(0, len(sampleArticle.shingles) - 1)] = \
                            random.randrange(-2 ** 64, 2 ** 64)
                    minhash_shingles([sampleArticle], hashfuncs)  # minhash the sample article
                    queryHash = LSH([sampleArticle], low, high)  # hash the sample article
                    candidates = set()
                    for key in queryHash.keys():
                        candidates.update(buckets.get(key, []))
                    for r in candidates:
                        if r == sampleArticle.ID:
                            foundArticle += 1
                            break

                print(
                    "found {}/10 plagiarized articles with M={},s_low={},s_high={}".format(foundArticle, k, low, high))
                # print("found candidates={} for randomized sample={}, with M={},s_low={},s_high={}".format(candidates,sampleArticle.ID,k, low,high))
