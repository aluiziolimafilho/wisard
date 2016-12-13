from random import randint

class RAM:

    def __init__(self, addressSize, entrySize, addressing):
        self.addressing = addressing
        self.ram = {}
        self.address = [ randint(0, entrySize-1) for x in range(addressSize) ]

    def _addressToIndex(self, entry):
        binCode = []
        for i in self.address:
            binCode.append(entry[i])
        return self.addressing(binCode)

    def _acumulateRam(self, index):
        if index not in self.ram:
            self.ram[index] = 0
        self.ram[index] += 1

    def _getValue(self, index):
        if index not in self.ram:
            return 0
        else:
            return self.ram[index]

    def train(self, entry):
        index = self._addressToIndex(entry)
        self._acumulateRam(index)

    def classify(self, entry):
        index = self._addressToIndex(entry)
        return self._getValue(index)
