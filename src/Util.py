import math
import random
import matplotlib.pyplot as plt

import csv
import ast

stopwords = {"ourselves", "hers", "between", "yourself", "but", "again", "there", "about", "once", "during", "out",
             "very", "having", "with", "they", "own", "an", "be", "some", "for", "do", "its", "yours", "such", "into",
             "of", "most", "itself", "other", "off", "is", "s", "am", "or", "who", "as", "from", "him", "each", "the",
             "themselves", "until", "below", "are", "we", "these", "your", "his", "through", "don", "nor", "me", "were",
             "her", "more", "himself", "this", "down", "should", "our", "their", "while", "above", "both", "up", "to",
             "ours", "had", "she", "all", "no", "when", "at", "any", "before", "them", "same", "and", "been", "have",
             "in", "will", "on", "does", "yourselves", "then", "that", "because", "what", "over", "why", "so", "can",
             "did", "not", "now", "under", "he", "you", "herself", "has", "just", "where", "too", "only", "myself",
             "which", "those", "i", "after", "few", "whom", "t", "being", "if", "theirs", "my", "against", "a", "by",
             "doing", "it", "how", "further", "was", "here", "than"}


class NewsArticle():
    def __init__(self, ID, content, preprocessing=True):
        self.ID = ID
        self.content = content
        self.shingles = []
        self.min_hashed_shingles = []

        if not preprocessing:
            self.tokens = list(dict.fromkeys(content.split()))
        else:

            content = content.casefold().replace(",", "").replace(".", "").replace("!","")  # casefolding and remove punctuations
            token = dict.fromkeys(content.split())
            for word in stopwords:
                token.pop(word, None)  # remove all frequent stopwords
            self.tokens = list(token)


def Jaccard_sim(set1, set2):
    if not isinstance(set1, set):
        set1 = set(set1)
    if not isinstance(set2, set):
        set2 = set(set2)

    intersec_size = len(set1.intersection(set2))
    union_size = (len(set1) + len(set2)) - intersec_size
    return intersec_size / union_size


def load_dataset_from_csv(filename, preprocess=True):
    with open(filename) as f:
        # cannot use a traditional csv reader as the content of article contains comma --> wrong column reading.
        f.readline()  # skip line 1
        parsing = f.readline()
        result = []
        while len(parsing) > 0:
            parsing = parsing.split(",", maxsplit=1)
            parsing[1] = parsing[1] \
                .strip().strip("\"")  # striping white spaces in the end, then strip unnecessary symbol
            assert (len(parsing) == 2)  # asserting column size
            result.append(NewsArticle(parsing[0], parsing[1], preprocess))  # we inherently know there are two columns
            parsing = f.readline()
        return result


def make_shingles(articles):
    for article in articles:
        for i in range(len(article.tokens) - 1):
            article.shingles.append(article.tokens[i] + " " + article.tokens[i + 1])


def hash_shingles(articles):
    for article in articles:
        for i in range(len(article.shingles)):
            article.shingles[i] = hash(article.shingles[i])

def hash_funcs(k):
    hash_funcs = []
    for i in range(k):
        hash_funcs.append(universal_hashing())
    return hash_funcs

def minhash_shingles(articles, hash_funcs):
    for article in articles:
        for j in range(len(hash_funcs)):
            for i in range(len(article.shingles)):
                article.shingles[i] = hash_funcs[j](article.shingles[i])
            article.min_hashed_shingles.append(min(article.shingles))


def calculateBestBandRowCombination(similarityThresholdLow, similarityThresholdHigh, signatureMatrixLength, boostHigh=1,
                                    boostLow=1):
    assert (isinstance(signatureMatrixLength, int))
    # calculate all integer divider of similarity Threshold
    root = math.ceil(math.sqrt(signatureMatrixLength))
    divisors = []
    for i in range(1, root + 1):
        if signatureMatrixLength % i == 0:
            divisors.append((i, int(signatureMatrixLength / i)))
            divisors.append((int(signatureMatrixLength / i), i))

    bestCombination = None
    bestLowHigh = None
    bestScore = 0
    for band, row in divisors:
        # maximize high similarity hashing chance while minimizing low similarity hashing chance
        hashChanceHigh = 1 - (1 - similarityThresholdHigh ** row) ** band
        hashChanceLow = 1 - (1 - similarityThresholdLow ** row) ** band
        score = hashChanceHigh * boostHigh - hashChanceLow / boostLow  # maximizing difference
        print(hashChanceHigh)
        if (score > bestScore):
            bestScore = score
            bestCombination = (band, row)
            bestLowHigh = (hashChanceLow, hashChanceHigh)

    print("low={},high={},band,row={}".format(bestLowHigh[0], bestLowHigh[1], bestCombination))
    return bestCombination


def LSH(articles, similarityLow, similarityHigh, hashFunction=hash):
    assert (len(articles) > 0)  # no empty matrix
    band, row = calculateBestBandRowCombination(similarityLow, similarityHigh, len(articles[0].min_hashed_shingles))
    assert (len(articles[0].min_hashed_shingles) == band * row)  # matrix length = band*row
    buckets = dict()
    for i in range(band):
        for article in articles:
            shingles = article.min_hashed_shingles
            shinglesInBand = shingles[i * row:(i + 1) * row]
            hashed = 0
            for obj in shinglesInBand:
                hashed = hashed + hashFunction(obj)  # add up multiple hash
            bucket = buckets.get(hashed, [])
            bucket.append(article.ID)
            buckets[hashed] = bucket  # put into bucket
    return buckets

def universal_hashing():
    def rand_prime():
        while True:
            p = random.randrange(2 ** 32, 2 ** 34, 2)
            if all(p % n != 0 for n in range(3, int((p ** 0.5) + 1), 2)):
                return p

    m = 2 ** 32 - 1
    p = rand_prime()
    a = random.randint(0, p)
    if a % 2 == 0:
        a += 1
    b = random.randint(0, p)

    def h(x):
        return ((a * x + b) % p) % m

    return h


def plot_bargraph(data):
    # creating the dataset
    courses = list(data.keys())
    values = list(data.values())

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(courses, values, color='royalblue',
            width=0.6)

    plt.xlabel("Similarity between articles(in %)")
    plt.ylabel("Number of articles")
    plt.title("Number of articles in function of their similarity with each other (using 1000 articles)")
    plt.show()


def write_buckets_to_csv(buckets):
    with open('lsh_buckets.csv', mode='w', newline='') as lsh_buckets:
        bucket_writer = csv.writer(lsh_buckets)
        for key, value in buckets.items():
            bucket_writer.writerow((key, value))


def load_bucket_from_csv(filename):
    with open(filename, mode='r') as lsh_buckets:
        bucket_reader = csv.reader(lsh_buckets)
        dict = {}
        for row in bucket_reader:
            dict[int(row[0])] = ast.literal_eval(row[1])
        return dict




def write_result_to_csv(results):
    with open('result.csv', mode='w',newline='') as result:
        result_writer = csv.writer(result)
        for item in results:
            result_writer.writerow((item[0],item[1]))

load_bucket_from_csv("lsh_buckets.csv")
