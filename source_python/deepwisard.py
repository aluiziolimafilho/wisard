import random

from discriminator import DeepDiscriminator
from inputfunctions import *

class BaseLayer:

    def __init__(self, deep=None, connectLayers=None):
        if isinstance(deep, BaseLayer):
            self.deep = deep
        else:
            self.deep = None

        if isinstance(connectLayers, ConnectLayersBase):
            self.connectLayers = connectLayers
        else:
            self.connectLayers = None

    def train(self, entry, aclass):
        if self.deep is not None and self.connectLayers is not None:
            self.deep.train(entry, aclass)
            featureVector = self.deep.classify(entry, aclass)
            entry = self.connectLayers.training(featureVector)
        self._train(entry, aclass)

    def classify(self, entry, aclass=None): # if aclass is not None then is the fase of trainning otherwise is the fase of classification
        if aclass is None:
            if self.deep is not None and self.connectLayers is not None:
                featuresVectors = self.deep.classify(entry)
                entry = self.connectLayers.classifying(featuresVectors)
            return self._classify(entry)
        else:
            return self._classifyTrain(entry, aclass)

    def _train(self, entry, aclass):
        pass

    def _classifyTrain(self, entry, aclass):
        pass

    def _classify(self, entry):
        pass

class LayerWisard(BaseLayer):

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

        BaseLayer.__init__(self, deep=deep, connectLayers=connectLayers)

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

        if sizeOfEntry is not None:
            for aclass in classes:
                self._createDiscriminator(aclass, sizeOfEntry)

    def _createDiscriminator(self, aclass, sizeOfEntry):
        self.discriminators[str(aclass)] = DeepDiscriminator(
            str(aclass), sizeOfEntry, self.addressSize,
            self.ramcontrols, self.numberOfDiscriminators, self.numberOfRAMS)

    def _train(self, entry, aclass):
        if aclass not in self.discriminators:
            self._createDiscriminator(aclass, len(entry))
        self.discriminators[aclass].train(entry)
        if self.ramcontrols.decayActivated:
            for key in self.discriminators:
                if key != aclass:
                    self.discriminators[key].train(entry, negative=True)

    def _classifyTrain(self, entry, aclass):
        return self.discriminators[aclass].classify(entry)

    def _classify(self, entry):
        out = {}
        for key in self.discriminators:
            if isinstance(entry, dict):
                out[key] = self.discriminators[key].classify(entry[key])
            else:
                out[key] = self.discriminators[key].classify(entry)

        return out
