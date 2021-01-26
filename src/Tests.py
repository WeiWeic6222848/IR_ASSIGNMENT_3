from Util import *

import unittest

class TestLoadingCSV(unittest.TestCase):

    def test_small(self):
        result=load_dataset_to_csv("dataset/news_articles_small.csv")
        self.assertEqual(1000,len(result))

if __name__ == '__main__':
    unittest.main()