from .binarization import *

class RAMControls:

    def __init__(self, base=2, decayActivated=False, alfa=lambda x: x + 1.0, beta=lambda x: x*0.1):
        self.decayActivated = decayActivated
        self.base=base
        self.alfa = alfa
        self.beta = beta

    def addressing(self, binCode):
        index = 0
        for i,e in enumerate(binCode):
            if e < self.base:
                index += e*pow(self.base,i)
            else:
                index += (self.base-1)*pow(self.base,i)
        return index

    def increase(self, **kwargs):
        index = kwargs['index']
        ram = kwargs['ram']
        value = ram[index]
        ram[index] = self.alfa(value)

    def decay(self, **kwargs):
        index = kwargs['index']
        ram = kwargs['ram']
        value = ram[index]
        ram[index] = self.beta(value)


class MakeBleachingSum:

    def __init__(self, cut=lambda x: x):
        self.cut = cut

    def __call__(self, discriminatorsoutput):
        for key in discriminatorsoutput:
            ramsoutput = discriminatorsoutput[key][0]
            discriminatorsoutput[key][1] = sum(map(self.cut,ramsoutput))
        return discriminatorsoutput

class MakeBleachingDefault:

    def __init__(self, bleachingActivated=True):
        self.bleachingActivated = bleachingActivated

    def __call__(self, discriminatorsoutput):
        bleaching = 0
        ambiguity = True
        biggestVote = 2
        while ambiguity and biggestVote > 1:
            bleaching += 1
            biggestVote = None
            ambiguity = False
            for key in discriminatorsoutput:
                discriminator = discriminatorsoutput[key]
                limit = lambda x: 1 if x > bleaching else 0
                discriminator[1] = sum(map(limit, discriminator[0]))
                if biggestVote is None or discriminator[1] > biggestVote:
                    biggestVote = discriminator[1]
                    ambiguity = False
                elif discriminator[1] == biggestVote:
                    ambiguity = True
            if self.bleachingActivated:
                break

        return discriminatorsoutput

class MakeBleachingClus:

    def __init__(self, bleachingActivated=True):
        self.bleachingActivated = bleachingActivated

    def __call__(self, discriminatorsoutput):
        bleaching = 0
        ambiguity = True
        biggestVote = 2
        while ambiguity and biggestVote > 1:
            bleaching += 1
            biggestVote = None
            ambiguity = False
            for key in discriminatorsoutput:
                cluster = discriminatorsoutput[key]
                for discriminator in cluster:
                    limit = lambda x: 1 if x > bleaching else 0
                    discriminator[1] = sum(map(limit, discriminator[0]))
                    if biggestVote is None or discriminator[1] > biggestVote:
                        biggestVote = discriminator[1]
                        ambiguity = False
                    elif discriminator[1] == biggestVote:
                        ambiguity = True
            if self.bleachingActivated:
                break

        return discriminatorsoutput
