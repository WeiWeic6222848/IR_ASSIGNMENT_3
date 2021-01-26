class NewsArticle():
    def __init__(self, ID, content):
        self.ID = ID
        self.content = content

        content = content.casefold().replace(",","").replace(".","")
        token = dict.fromkeys(content.split())
        for word in stopwords:
            token.pop(word, None)  # remove all frequent stopwords

        self.token = list(token)

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




loaded=load_dataset_to_csv("dataset/news_articles_small.csv")
article = loaded[0]
print(article.token)
