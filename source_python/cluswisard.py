import random

from cluster import Cluster
from inputfunctions import *

class ClusWisard():

    def __init__(self, **kwargs):
        self.addressSize = kwargs.get('addressSize')
        self.minScore = kwargs.get('minScore',2)
        self.threshold = kwargs.get('threshold', 5)
        self.seed = kwargs.get('seed', random.randint(0, 1000000))
        random.seed(self.seed)
        self.verbose = kwargs.get('verbose')

        self.clusters = {}

    def _createCluster(self, entrySize):
        return Cluster(id=len(self.clusters)+1 ,addressSize=self.addressSize, entrySize=entrySize, ramcontrols=RAMControls())

    def train(self, entry):
        pass

    def trainall(self, entries):
        for i,entry in enumerate(entries):
            if self.verbose is not None:
                self.verbose(fase="training", index=i+1, total=len(entries), end=i==len(entries)-1)
            aclass = str(classes[i])
            self.train(entry, aclass)

    def classifyall(self, entries):
        pass
