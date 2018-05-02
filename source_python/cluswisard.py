import random

from cluster import Cluster
from inputfunctions import *

class ClusWisard():

    def __init__(self, **kwargs):
        self.addressSize = kwargs.get('addressSize')
        self.minScore = kwargs.get('minScore',2)
        self.threshold = kwargs.get('threshold', 5)
        self.makeBleaching = kwargs.get('makeBleaching', MakeBleachingClus(True))
        self.seed = kwargs.get('seed', random.randint(0, 1000000))
        random.seed(self.seed)
        self.verbose = kwargs.get('verbose')

        self.clusters = {}

    def _createCluster(self, entrySize):
        return Cluster(
            minScore=self.minScore,
            threshold=self.threshold,
            addressSize=self.addressSize,
            entrySize=entrySize,
            ramcontrols=RAMControls())

    def train(self, entry, aClass):
        if aClass not in self.clusters:
            self.clusters[aClass] = self._createCluster(len(entry))
        self.clusters[aClass].train(entry)

    def trainall(self, entries, classes):
        for i,entry in enumerate(entries):
            if self.verbose is not None:
                self.verbose(fase="training", index=i+1, total=len(entries), end=i==len(entries)-1)
            aclass = str(classes[i])
            self.train(entry, aclass)

    def _getDiscriminatorsOutput(self, entry):
        output = {}
        for key in self.clusters:
            cluster = self.clusters[key]
            output[key] = []
            for d in cluster.classify(entry):
                output[key].append([d, 0])
        return output

    def classify(self, entry):
        output = self._getDiscriminatorsOutput(entry)
        output = self.makeBleaching(output)
        classe = max(output, key=lambda x: max(output[x], key=lambda y: y[1]))
        return classe

    def classifyall(self, entries):
        outputs = []
        for i,entry in enumerate(entries):
            if self.verbose is not None:
                self.verbose(fase="classifing", index=i+1, total=len(entries), end=i==len(entries)-1)
            aClass = self.classify(entry)
            outputs.append(aClass)
        return outputs

    def getMentalImages(self):
        images = {}
        for key in self.clusters:
            c = self.clusters[key]
            images[key] = c.getMentalImages()
        return images
