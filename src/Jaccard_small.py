from Util import *


loaded=load_dataset_to_csv("dataset/news_articles_small.csv")

make_shingles(loaded)

hash_shingles(loaded)

minhash_shingles(loaded,20)

jac_sim = []

plot_bargraph(jac_sim)

