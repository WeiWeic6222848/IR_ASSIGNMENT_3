from Util import *


def calculate_jacc_sim(self):
    pass


if __name__ == '__main__':
    data = load_dataset_to_csv("dataset/news_articles_small.csv")
    make_shingles(data)
    hash_shingles(data)
    d = {"0-10":0,
         "10-20":0,
         "20-30":0,
         "30-40": 0,
         "40-50": 0,
         "50-60": 0,
         "60-70": 0,
         "70-80": 0,
         "80-90": 0,
         "90-100": 0,
         }
    for article1 in data:
        for article2 in data:
            if article1 != article2:
                sim = Jaccard_sim(article1.shingles,article2.shingles)
                if sim < 0.10:
                    d["0-10"] += 1
                elif sim <0.20:
                    d["10-20"] += 1
                elif sim < 0.30:
                    d["20-30"] += 1
                elif sim <0.40:
                    d["30-40"] += 1
                elif sim < 0.50:
                    d["40-50"] += 1
                elif sim <0.60:
                    d["50-60"] += 1
                elif sim < 0.70:
                    d["60-70"] += 1
                elif sim <0.80:
                    d["70-80"] += 1
                elif sim < 0.90:
                    d["80-90"] += 1
                else:
                    d["90-100"] += 1

    breakpoint()
