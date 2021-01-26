class NewsArticle():
    def __init__(self, ID, content):
        self.ID = ID
        self.content = content


def load_dataset_to_csv(filename):
    with open(filename) as f:
        f.readline()  # skip line 1
        parsing = f.readline()
        result = []
        while len(parsing)>0:
            parsing = parsing.split(",")
            result.append(NewsArticle(parsing[0], parsing[1]))
            parsing = f.readline()
        return result



print(len(load_dataset_to_csv("dataset/news_articles_small.csv")))
