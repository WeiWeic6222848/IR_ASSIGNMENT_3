class NewsArticle():
    def __init__(self,ID, content, tokens):
        self.ID= ID
        self.content= content
        self.tokens = tokens
        self.shingles = []
        self.min_hashed_shingles = []
        content = content.casefold().replace(",","").replace(".","")
        token = dict.fromkeys(content.split())
        for word in stopwords:
            token.pop(word, None)  # remove all frequent stopwords

        self.token = list(token)

def Jaccard_sim(set1, set2):
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

def hash_k(k,number):
    return number % (1000000*k)

def minhash_shingles(articles,k): #k = number of hash functions to use
    for article in articles:
        for j in range(k):
            for i in range(len(article.shingles)):
                article.shingles[i] = hash_k(j+1,article.shingles[i])
            article.min_hashed_shingles.append(min(article.shingles))



#test
na = NewsArticle(1,"The quick brown fox",["The","quick","brown","fox"])
na2 = NewsArticle(2,"The lazy blue fox",["The", "lazy", "blue", "fox"])
result=[na,na2]
make_shingles(result)
hash_shingles(result)
minhash_shingles(result,8)

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

print(na.shingles[0])

#print(len(load_dataset_to_csv("dataset/news_articles_small.csv")))
#result = load_dataset_to_csv("dataset/news_articles_small.csv")






loaded=load_dataset_to_csv("dataset/news_articles_small.csv")
article = loaded[0]
print(article.token)
