import random

from discriminator import Discriminator
from deepwisard import LayerWisard, ConnectLayersDefault
from inputfunctions import *

class Wisard:

    def __init__(self,
            addressSize = 3,
            numberOfRAMS = None,
            bleachingActivated = True,
            sizeOfEntry = None,
            classes = [],
            seed = random.randint(0, 1000000),
            verbose = None,
            makeBleaching = None,
            ramcontrols = None,
            deep = None,
            connectLayers = ConnectLayersDefault()):

        self.seed = seed
        self.verbose = verbose
        random.seed(seed)

        if addressSize < 3:
            self.addressSize = 3
        else:
            self.addressSize = addressSize
        self.numberOfRAMS = numberOfRAMS
        self.discriminators = {}

        if isinstance(ramcontrols, RAMControls):
            self.ramcontrols = ramcontrols
        else:
            self.ramcontrols = RAMControls()

        if makeBleaching is None:
            self.makeBleaching = MakeBleachingDefault(bleachingActivated)
        else:
            self.makeBleaching = makeBleaching

        if isinstance(deep, LayerWisard):
            self.deep = deep
        else:
            self.deep = None

        self.connectLayers = connectLayers

        if sizeOfEntry is not None:
            for aclass in classes:
                self._createADiscriminator(aclass, sizeOfEntry)

    def _createADiscriminator(self, aclass, sizeOfEntry):
        self.discriminators[str(aclass)] = Discriminator(
            str(aclass), sizeOfEntry, self.addressSize,
            self.ramcontrols, self.numberOfRAMS)

    def _trainOneEntry(self, entry, aclass):
        self.discriminators[aclass].train(entry)
        if self.ramcontrols.decayActivated:
            for key in self.discriminators:
                if key != aclass:
                    self.discriminators[key].train(entry, negative=True)

    def _trainDeep(self, entry, aclass):
        if self.deep is not None and self.connectLayers is not None:
            self.deep.train(entry, aclass)
            featureVector = self.deep.classify(entry)
            entry = self.connectLayers(featureVector)
        return entry

    def train(self, entries, classes):
        for i,entry in enumerate(entries):
            if self.verbose is not None:
                self.verbose(fase="training", index=i+1, total=len(entries), end=i==len(entries)-1)

            aclass = str(classes[i])
            entry = self._trainDeep(entry, aclass)

            if aclass not in self.discriminators:
                self._createADiscriminator(aclass, len(entry))
            self._trainOneEntry(entry, aclass)

    def getDiscriminatorsOutput(self, entry):
        discriminatorsoutput = {}
        for keyClass in self.discriminators:
            discriminatorsoutput[keyClass] = [self.discriminators[keyClass].classify(entry),0]
        return discriminatorsoutput


    def _deepClassify(self, entry):
        if self.deep is not None and self.connectLayers is not None:
            featureVector = self.deep.classify(entry)
            entry = self.connectLayers(featureVector)
        return entry

    def classifyEntry(self, entry):
        entry = self._deepClassify(entry)
        discriminatorsoutput = self.getDiscriminatorsOutput(entry)

        discriminatorsoutput = self.makeBleaching(discriminatorsoutput)
        calc = lambda key: (key, float(discriminatorsoutput[key][1])/len(discriminatorsoutput[key][0]))
        classes = list(map(calc,discriminatorsoutput))
        classes.sort(key=lambda x: x[1], reverse=True)
        return classes


    def classify(self, entries):
        output=[]
        for i,entry in enumerate(entries):
            if self.verbose is not None:
                self.verbose(fase="training", index=i+1, total=len(entries), end=i==len(entries)-1)
            aclass = self.classifyEntry(entry)[0][0]
            output.append((entry, aclass))
        return output
