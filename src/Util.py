import random
import matplotlib.pyplot as plt
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
    def __init__(self,ID, content):
        self.ID= ID
        self.content= content
        self.shingles = []
        self.min_hashed_shingles = []
        content = content.casefold().replace(",","").replace(".","")
        tokens = dict.fromkeys(content.split())
        for word in stopwords:
            tokens.pop(word, None)  # remove all frequent stopwords

        self.tokens = list(tokens)

def Jaccard_sim(set1, set2):
    if not isinstance(set1,set):
        set1 = set(set1)
    if not isinstance(set2,set):
        set2 = set(set2)

    intersec_size = len(set1.intersection(set2))
    union_size = (len(set1)+len(set2)) - intersec_size
    return intersec_size/union_size

def load_dataset_to_csv(filename):
    with open(filename) as f:
        f.readline()  # skip line 1
        parsing = f.readline()
        result = []
        while len(parsing) > 0:
            parsing = parsing.split(",", maxsplit=1)
            parsing[1] = parsing[1].strip().strip("\"")
            result.append(NewsArticle(parsing[0], parsing[1]))
            parsing = f.readline()
        return result

def make_shingles(articles):
    for article in articles:
        for i in range(len(article.tokens)-1):
            article.shingles.append(article.tokens[i]+" "+article.tokens[i+1])

def hash_shingles(articles):
    for article in articles:
        for i in range(len(article.shingles)):
            article.shingles[i] = hash(article.shingles[i])

def minhash_shingles(articles,k): #k = number of hash functions to use
    hash_funcs = []
    for i in range(k):
        hash_funcs.append(universal_hashing())

    for article in articles:
        for j in range(k):
            for i in range(len(article.shingles)):
                article.shingles[i] = hash_funcs[j](article.shingles[i])
            article.min_hashed_shingles.append(min(article.shingles))


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

def plot_bargraph(jac_sim):
    # creating the dataset
    data = {'0-10': 20, '10-20': 15, '20-30': 30,'30-40': 30,'40-50': 30,'50-60': 30,'60-70': 30,'70-80': 30,'80-90': 30, '90-100': 30}
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


loaded=load_dataset_to_csv("dataset/news_articles_small.csv")
make_shingles(loaded)
hash_shingles(loaded)
minhash_shingles(loaded,20)
