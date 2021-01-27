import os

from Util import *

import unittest
import tempfile
class TestLoadingCSV(unittest.TestCase):

    def test_small(self):
        result=load_dataset_from_csv("dataset/news_articles_small.csv")
        self.assertEqual(1000,len(result))
        self.assertEqual("Scoreboard on the second day of a four day match between Australia and a West Indies Cricket Board of Control President's XI here Sunday. BATTING--MOrdonez, Detroit, .383; ISuzuki, Seattle, .358; Posada, New York, .345; Jeter, New York, .343; Polanco, Detroit, .339; Willits, Los Angeles, .337; OCabrera, Los Angeles, .337. Iranian Foreign Minister Manouchehr Mottaki met with UN atomic watchdog chief Yukiya Amano in Vienna on Sunday, but there appeared to be no immediate breakthrough on a stalled nuclear fuel deal. Among the many theories held by the Latin-music bandleader, pianist and ideologue Eddie Palmieri, is this: The less you eat, the more power you have. ``See, we're essentially an air-gas engine,'' he said. ``The less encumbrance in the organism, the more vitality.'' So at a lunch meeting this month, Press freedom is deteriorating in the former Soviet republic of Azerbaijan, the international media watchdog Reporters Without Borders (RSF) said Friday. Of the two brothers who created \"\"Love and Rockets,\"\" the punk-era comic series that's arguably the genre's most influential work of its day, Gilbert Hernandez is widely considered the John Lennon figure -- the driven, \"\"serious artist,\"\" allergic to superficiality and attracted by ugliness as well as beauty. Paul Gigot, who won the Pulitzer Prize for commentary last year, has been named editor of The Wall Street Journal's editorial page, the paper's publisher, Dow Jones &amp; Co., announced Wednesday. More than 100 foreigners working in Xining, the capital of northwest China's Qinghai Province, were recently invited by local Tibetans to taste the homemade cheese they produce from yak's milk."
                         ,result[828].content)
        self.assertEqual("Heavy snowfall and strong winds on Monday disrupted central city traffic and caused delays of up to 30 minutes at the Stockholm airport, airport officials said. Suspected Taliban militants attacked police posts in southern Afghanistan, sparking clashes and NATO airstrikes that left 25 civilians and 20 militants dead, a senior police officer said Friday. Unheralded Marcus Fraser landed the biggest victory of his career after he carded a final-round three-under-par 69 to win the Ballantine's Championship on Sunday. Vivendi Universal said Monday that it would ask a Paris court to annul the voting results of its shareholder meeting last Wednesday. US communications giant Motorola Inc on Friday launched an applied research laboratory in India's high-tech hub Bangalore, as part of a plan to make the growing Asian nation its center for engineering and product development. They also released a chilling timeline and grim details of Tyler Peterson pursuing his victims through his former girlfriend's house, killing one girl as she hid in a closet. Two defectors from Belarus have told U.S. officials that a death squad created by President Alexander Lukashenko's government was responsible for the disappearance of four prominent opposition figures over the past two years in Belarus, the State Department said Wednesday. Hasina who will leave here early Saturday for a three-nation Europe tour will pay an official visit to Germany from December 5 to 7 at the invitation of the Federal Chancellor."
                         ,result[851].content)
        self.assertEqual("11",result[11].ID)

    def test_large(self):
        result=load_dataset_from_csv("dataset/news_articles_large.csv")
        self.assertEqual(10000,len(result))
        self.assertEqual("Jason Miller, 17, was among the fans who came to see Tyson released. \"\"We just came because he's the greatest fighter of all time and he was held unjustly,\"\" Miller said. A U.S. judge has dismissed wrongful death claims brought against Drummond Co. for its alleged links to the killings of three union leaders at the Alabama coal company's huge mine in Colombia. Paul Schaefer, a former Nazi corporal and founder of a mysterious German enclave in southern Chile, died Saturday in a prison hospital where he was serving 20 years for sexually abusing children, prison officials said. Bring back the goons. Seriously. Make 'em wear court jesters' outfits with clanging bells and fool's caps, and let 'em grapple and maul like in the good old days, a few years ago. The requiem mass for the funeral Friday of Pope John Paul II will follow centuries of solemn ritual befitting the final farewell to the head of the Roman Catholic Church. A new study of state achievement tests offers evidence that the No Child Left Behind law's core mission -- to push all students to score well in reading and math -- is undermined by wide variations in how states define a passing score. Jeff Weaver retired 18 in a row after escaping a bases-loaded threat and pitched into the eighth inning on a hot, muggy night, leading the Detroit Tigers to a 3-1 victory Tuesday over the Cincinnati Reds. Republican George W. Bush said Sunday night that he and Dick Cheney will undertake the responsibility of preparing to serve as the next president and vice president of the United States."
                         ,result[11].content)
        self.assertEqual("11",result[11].ID)

    def test_custom(self):
        new_file, filename = tempfile.mkstemp()
        os.write(new_file, b"News_ID,article\n0,test\n1,hello,world\n100,0\n")
        result = load_dataset_from_csv(filename)
        self.assertEqual(3,len(result))
        self.assertEqual("test",result[0].content)
        self.assertEqual("0",result[0].ID)


class TestJaccardSim(unittest.TestCase):
    def test_normal(self):
        set1 = {1,4,5,6}
        set2 = {5,8,9,10}
        self.assertEqual(1/7,Jaccard_sim(set1,set2))

    def test_not_similar(self):
        set1 = {1,2,3,4}
        set2 = {5,6,7,8,9,10}
        self.assertEqual(0,Jaccard_sim(set1,set2))

    def test_duplicate(self):
        set1 = {1,2,3,4}
        set2 = {1,2,3,4}
        self.assertEqual(1,Jaccard_sim(set1,set2))

    def test_using_list_instead_of_set(self):
        set1 = [1, 4, 5, 6, 8]
        set2 = [5, 8, 9, 10]
        self.assertEqual(2 / 7, Jaccard_sim(set1, set2))

    def test_using_tuple_instead_of_set(self):
        set1 = (1, 4, 5, 6)
        set2 = (5, 8, 9, 10, 4 ,6)
        self.assertEqual(3 / 7, Jaccard_sim(set1, set2))

class TestLSH(unittest.TestCase):
    def test1(self):
        loaded=load_dataset_from_csv("dataset/news_articles_small.csv")
        make_shingles(loaded)
        hash_shingles(loaded)
        minhash_shingles(loaded, 20)
        bucketed = LSH(loaded, 0.3, 0.8)
        write_buckets_to_csv(bucketed)
        print(bucketed)

if __name__ == '__main__':
    unittest.main()