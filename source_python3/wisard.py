import random
import numpy as np

class WiSARD:

    def __init__(self,
            addressSize = 3,
            numberOfRAMS = None,
            bleachingActivated = True,
            seed = random.randint(0, 1000000),
            verbose = True):

        self.seed = seed
        self.verbose = verbose
        np.random.seed(seed)
        self.rams = []
        if addressSize < 2:
            self.addressSize = 3
        else:
            self.addressSize = addressSize
        self.numberOfRAMS = numberOfRAMS
        self.discriminators = {}
        self.bleachingActivated = bleachingActivated

    def _getRAMPosition(self, address):
        index = 0
        for i,e in enumerate(address):
            if e > 0:
                index += pow(2,i)
        return index


    def _trainEntry(self, entry, aclass):
        discriminator = self.discriminators[aclass]
        for ram in discriminator:
            code = []
            for i in ram['address']:
                code.append(entry[i])
            index = self._getRAMPosition(code)
            ram['ram'][index] += 1


    def _setNumberOfRAMS(self, entrySize):
        minimumOfRAMS = 4
        if self.numberOfRAMS is None or self.numberOfRAMS < minimumOfRAMS:
            self.numberOfRAMS = int(entrySize/self.addressSize)
            if self.numberOfRAMS < minimumOfRAMS:
                self.numberOfRAMS = minimumOfRAMS


    def _createDiscriminator(self, entrySize):
        self._setNumberOfRAMS(entrySize)
        rams = []
        for i in range(self.numberOfRAMS):
            address = np.random.randint(entrySize, size=self.addressSize)
            positions = np.zeros(pow(2,self.addressSize), dtype=np.long)
            ram = {'address': address, 'ram': positions}
            rams.append(ram)
        rams = np.array(rams)
        return rams

    def train(self, entries, classes):
        sizeOfEntry = len(entries[0])
        for i,entry in enumerate(entries):
            if self.verbose:
                print("\rtraining "+str(i+1)+" of "+str(len(entries)), end='')
            aclass = str(classes[i])
            if aclass not in self.discriminators:
                self.discriminators[aclass] = self._createDiscriminator(sizeOfEntry)
            self._trainEntry(entry, aclass)
        if self.verbose:
            print("\r")

    def _getBiggestVote(self, discriminatorsoutput):
        biggestVote = None
        ambiguity = False
        for key in discriminatorsoutput:
            discriminatorvotes = discriminatorsoutput[key][1]
            if biggestVote is None or discriminatorvotes > biggestVote:
                biggestVote = discriminatorvotes
                ambiguity = False
            elif discriminatorvotes == biggestVote:
                ambiguity = True

        return (biggestVote,ambiguity)


    def classifyEntry(self, entry, fixed_bleaching=None):
        classes = []
        discriminatorsoutput = {}
        bleaching = 1
        for keyClass in self.discriminators:
            discriminator = self.discriminators[keyClass]
            ramsoutput = []
            votes = 0
            for ram in discriminator:
                code = []
                for i in ram['address']:
                    code.append(entry[i])
                index = self._getRAMPosition(code)
                ramsoutput.append(ram['ram'][index])
                if fixed_bleaching is None:
                    if ram['ram'][index] >= bleaching:
                        votes += 1
                elif ram['ram'][index] >= fixed_bleaching:
                    votes += 1
            classes.append((keyClass, float(votes)/len(ramsoutput)))
            discriminatorsoutput[keyClass] = [ramsoutput, votes]

        if self.bleachingActivated and fixed_bleaching is None:
            biggestVote, ambiguity = self._getBiggestVote(discriminatorsoutput)
            while ambiguity and biggestVote > 1:
                bleaching += 1
                classes = []
                for key in discriminatorsoutput:
                    discriminator = discriminatorsoutput[key]
                    discriminator[1] = 0
                    for i in discriminator[0]:
                        if i >= bleaching:
                            discriminator[1] += 1
                    classes.append((key, float(discriminator[1])/len(discriminator[0])))
                biggestVote, ambiguity = self._getBiggestVote(discriminatorsoutput)
        classes.sort(key=lambda x: x[1], reverse=True)
        return classes

    def classify(self, entries, fixed_bleaching=None):
        output=[]
        for i,entry in enumerate(entries):
            if self.verbose:
                print("\rclassifying "+str(i+1)+" of "+str(len(entries)), end='')
            aclass = self.classifyEntry(entry,fixed_bleaching=fixed_bleaching)[0][0]
            output.append((entry, aclass))
        if self.verbose:
            print("\r")
        return output
