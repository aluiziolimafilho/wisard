import random

from discriminator import DeepDiscriminator
from inputfunctions import *

class ConnectLayersDefault:

    def __call__(self, featureVector):
        average = sum(featureVector)/len(featureVector)
        cut = lambda x: 1 if x > average else 0
        return list(map(cut,featureVector))

class LayerWisard:

    def __init__(self,
            addressSize = 3,
            numberOfRAMS = None,
            sizeOfEntry = None,
            classes = [],
            numberOfDiscriminators = 10, # number of discriminators for each class
            seed = random.randint(0, 1000000),
            verbose = None,
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
        self.numberOfDiscriminators = numberOfDiscriminators

        if isinstance(ramcontrols, RAMControls):
            self.ramcontrols = ramcontrols
        else:
            self.ramcontrols = RAMControls()

        if isinstance(deep, LayerWisard):
            self.deep = deep
        else:
            self.deep = None

        self.connectLayers = connectLayers

        if sizeOfEntry is not None:
            for aclass in classes:
                self._createADiscriminator(aclass, sizeOfEntry)

    def _createADiscriminator(self, aclass, sizeOfEntry):
        self.discriminators[str(aclass)] = DeepDiscriminator(
            str(aclass), sizeOfEntry, self.addressSize,
            self.ramcontrols, self.numberOfDiscriminators, self.numberOfRAMS)

    def _trainDeep(self, entry, aclass):
        if self.deep is not None and self.connectLayers is not None:
            self.deep.train(entry, aclass)
            featureVector = self.deep.classify(entry)
            entry = self.connectLayers(featureVector)
        return entry

    def train(self, entry, aclass):
        entry = self._trainDeep(entry, aclass)
        if aclass not in self.discriminators:
            self._createADiscriminator(aclass, len(entry))
        self.discriminators[aclass].train(entry)
        if self.ramcontrols.decayActivated:
            for key in self.discriminators:
                if key != aclass:
                    self.discriminators[key].train(entry, negative=True)

    def classify(self, entry):
        if self.deep is not None and self.connectLayers is not None:
            featureVector = self.deep.classify(entry)
            entry = self.connectLayers(featureVector)
        out = []
        for key in self.discriminators:
            out += self.discriminators[key].classify(entry)
        return out
