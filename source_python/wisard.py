import random

from discriminator import Discriminator
from inputfunctions import *

class WiSARD:

    def __init__(self,
            addressSize = 3,
            numberOfRAMS = None,
            bleachingActivated = True,
            seed = random.randint(0, 1000000),
            sizeOfEntry = None,
            classes = [],
            verbose = None,
            makeBleaching = None,
            increase = Increase(),
            decay = None,
            addressing = Addressing()):

        self.seed = seed
        self.verbose = verbose
        random.seed(seed)

        if addressSize < 3:
            self.addressSize = 3
        else:
            self.addressSize = addressSize
        self.numberOfRAMS = numberOfRAMS
        self.discriminators = {}
        self.bleachingActivated = bleachingActivated
        self.addressing = addressing
        self.increase = increase
        self.decay = decay
        if makeBleaching is None:
            self.makeBleaching = MakeBleachingDefault(bleachingActivated)
        else:
            self.makeBleaching = makeBleaching

        if sizeOfEntry is not None:
            for aclass in classes:
                self.discriminators[aclass] = Discriminator(
                    aclass, sizeOfEntry, self.addressSize,
                    self.addressing, self.increase, self.decay, self.numberOfRAMS)

    def train(self, entries, classes):
        sizeOfEntry = len(entries[0])
        for i,entry in enumerate(entries):
            if self.verbose is not None:
                self.verbose("training",i+1,len(entries), i==len(entries)-1)
            aclass = str(classes[i])
            if aclass not in self.discriminators:
                self.discriminators[aclass] = Discriminator(
                    aclass, sizeOfEntry, self.addressSize,
                    self.addressing, self.increase, self.decay, self.numberOfRAMS)
            self.discriminators[aclass].train(entry)
            if self.decay is not None:
                for key in self.discriminators:
                    if key != aclass:
                        self.discriminators[key].train(entry, negative=True)

    def classifyEntry(self, entry):
        discriminatorsoutput = {}
        for keyClass in self.discriminators:
            discriminatorsoutput[keyClass] = [self.discriminators[keyClass].classify(entry),0]
        discriminatorsoutput = self.makeBleaching(discriminatorsoutput)
        calc = lambda key: (key, float(discriminatorsoutput[key][1])/len(discriminatorsoutput[key][0]))
        classes = list(map(calc,discriminatorsoutput))
        classes.sort(key=lambda x: x[1], reverse=True)
        return classes


    def classify(self, entries):
        output=[]
        for i,entry in enumerate(entries):
            if self.verbose is not None:
                self.verbose("classifing",i+1,len(entries), i==len(entries)-1)
            aclass = self.classifyEntry(entry)[0][0]
            output.append((entry, aclass))
        return output
