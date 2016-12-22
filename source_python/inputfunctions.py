from binarization import *

class RAMControls:

    def __init__(self, base=2, decayActivated=False):
        self.decayActivated = decayActivated
        self.base=base

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
        ram[index] += 1

    def decay(self, **kwargs):
        index = kwargs['index']
        ram = kwargs['ram']
        if index in ram:
            value = ram[index]
            ram[index] = 0.5*value - 0.1

class MakeBleachingSum:

    def __call__(self, discriminatorsoutput):
        for key in discriminatorsoutput:
            ramsoutput = discriminatorsoutput[key][0]
            discriminatorsoutput[key][1] = sum(ramsoutput)
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
                limit = lambda x: 1 if x >= bleaching else 0
                discriminator[1] = sum(map(limit, discriminator[0]))
                if biggestVote is None or discriminator[1] > biggestVote:
                    biggestVote = discriminator[1]
                    ambiguity = False
                elif discriminator[1] == biggestVote:
                    ambiguity = True
            if self.bleachingActivated:
                break

        return discriminatorsoutput


class ConnectLayersDefault:

    def __init__(self):
        self.bin = BinarizationDefault()

    def join(self, matrix):
        out = []
        for line in matrix:
            for element in line:
                out.append(element)
        return out

    def __call__(self, featureVector):
        if len(featureVector) == 1:
            output = self.join(featureVector.items()[0][1])
            output = self.bin(output)
        else:
            output = {}
            for aclass in featureVector:
                output[aclass] = self.bin(self.join(featureVector[aclass]))
        return output
