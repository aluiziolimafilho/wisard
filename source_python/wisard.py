import random

from discriminator import Discriminator
from deepwisard import LayerWisard, ConnectLayersDefault, BaseLayer
from inputfunctions import *

class Wisard(BaseLayer):

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

        if isinstance(ramcontrols, RAMControls):
            self.ramcontrols = ramcontrols
        else:
            self.ramcontrols = RAMControls()

        if makeBleaching is None:
            self.makeBleaching = MakeBleachingDefault(bleachingActivated)
        else:
            self.makeBleaching = makeBleaching

        if sizeOfEntry is not None:
            for aclass in classes:
                self._createDiscriminator(aclass, sizeOfEntry)

    def _createDiscriminator(self, aclass, sizeOfEntry):
        self.discriminators[str(aclass)] = Discriminator(
            str(aclass), sizeOfEntry, self.addressSize,
            self.ramcontrols, self.numberOfRAMS)

    def _train(self, entry, aclass):
        if aclass not in self.discriminators:
            self._createDiscriminator(aclass, len(entry))
        self.discriminators[aclass].train(entry)
        if self.ramcontrols.decayActivated:
            for key in self.discriminators:
                if key != aclass:
                    self.discriminators[key].train(entry, negative=True)

    def trainall(self, entries, classes):
        for i,entry in enumerate(entries):
            if self.verbose is not None:
                self.verbose(fase="training", index=i+1, total=len(entries), end=i==len(entries)-1)
            aclass = str(classes[i])
            self.train(entry, aclass)

    def getDiscriminatorsOutput(self, entry):
        discriminatorsoutput = {}
        if isinstance(entry,dict):
            for keyClass in entry:
                discriminatorsoutput[keyClass] = [self.discriminators[keyClass].classify(entry[keyClass]),0]
        else:
            for keyClass in self.discriminators:
                discriminatorsoutput[keyClass] = [self.discriminators[keyClass].classify(entry),0]
        return discriminatorsoutput


    def _classify(self, entry):
        discriminatorsoutput = self.getDiscriminatorsOutput(entry)
        discriminatorsoutput = self.makeBleaching(discriminatorsoutput)
        classe = max(discriminatorsoutput, key=lambda x: discriminatorsoutput[x][1])
        return classe


    def classifyall(self, entries):
        output=[]
        for i,entry in enumerate(entries):
            if self.verbose is not None:
                self.verbose(fase="training", index=i+1, total=len(entries), end=i==len(entries)-1)
            aclass = self.classify(entry)
            output.append(aclass)
        return output
