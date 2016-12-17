

class Addressing:
    def __call__(self, binCode): # binCode is a list of values of selected points of entry
        index = 0
        for i,e in enumerate(binCode):
            if e > 0:
                index += pow(2,i)
        return index

class Decay:

    def __call__(self, **kwargs):
        index = kwargs['index']
        ram = kwargs['ram']
        if index in ram:
            value = ram[index]
            ram[index] = 0.5*value - 0.1

class Increase:

    def __call__(self, **kwargs):
        index = kwargs['index']
        ram = kwargs['ram']
        if index not in ram:
            ram[index] = 0
        ram[index] += 1

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
