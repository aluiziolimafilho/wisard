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
        if addressSize < 3:
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

    def _getRAM(self, ram, index):
        if index not in ram['ram']:
            return 0
        else:
            return ram['ram'][index]

    def _acumRAM(self, ram, index):
        if index not in ram['ram']:
            ram['ram'][index] = 0
        ram['ram'][index] += 1



    def _trainEntry(self, entry, aclass):
        discriminator = self.discriminators[aclass]
        for ram in discriminator:
            code = []
            for i in ram['address']:
                code.append(entry[i])
            index = self._getRAMPosition(code)
            self._acumRAM(ram, index)


    def _setNumberOfRAMS(self, entrySize):
        if self.numberOfRAMS is None:
            self.numberOfRAMS = int(entrySize/self.addressSize)


    def _createDiscriminator(self, entrySize):
        self._setNumberOfRAMS(entrySize)
        rams = []
        for i in range(self.numberOfRAMS):
            address = np.random.randint(entrySize, size=self.addressSize)
            ram = {'address': address, 'ram': {}}
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
                ramsoutput.append(self._getRAM(ram, index))
                if fixed_bleaching is None:
                    if self._getRAM(ram, index) >= bleaching:
                        votes += 1
                elif self._getRAM(ram, index) >= fixed_bleaching:
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
