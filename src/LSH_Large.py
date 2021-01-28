from Util import *

from Util import *


def write_result_to_csv(results):
    with open('result.csv', mode='w', newline='') as result:
        result_writer = csv.writer(result)
        for item in results:
            result_writer.writerow((item[0], item[1]))


if __name__ == "__main__":
    # load, and process the smalldataset
    data = load_dataset_from_csv("dataset/news_articles_large.csv")
    make_shingles(data)
    hash_shingles(data)
    minhash_shingles(data, hash_funcs(40))  # M=40
    buckets = LSH(data, 0.3, 0.8, preferRecall=True)  # s1=0.3,s2=0.8, maximize recall -> b=10, r=4
    result = []
    for candidate in buckets.values():
        # iterate through each of the buckets
        if len(candidate) > 1:
            # if there are more than one element
            for i1 in range(len(candidate)):
                print(int(candidate[i1]))
                article1 = data[int(candidate[i1])]  # assume ID = row ID
                for i2 in range(i1+1, len(candidate)):
                    print(int(candidate[i2]))
                    article2 = data[int(candidate[i2])]  # assume ID = row ID

                    # calculate Jaccard index
                    score = Jaccard_sim(article1.shingles, article2.shingles)
                    # if Jaccard index is bigger than 0.8, add to result
                    if score >= 0.8:
                        result.append((article1.ID, article2.ID))
    write_result_to_csv(result)
