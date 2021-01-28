from Util import *
from copy import deepcopy
from math import inf
import sys

from Util import *

MatrixSizes = [30]
similarityLow = [0.1, 0.4, 0.5]
similarityHigh = [0.7, 0.8]
similarityThreshHolds = [0.7, 0.8, 0.9]

random.seed(0)
sampleSize = 1000
if __name__ == "__main__":
    for low in similarityLow:
        for high in similarityHigh:
            calculateBestBandRowCombination(low,high,40)