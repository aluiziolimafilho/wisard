from random import randint

class RAM:

    def __init__(self, addressSize, entrySize, controls):
        self.controls = controls
        self.ram = {}
        self.address = [ randint(0, entrySize-1) for x in range(addressSize) ]

    def _addressToIndex(self, entry):
        binCode = []
        for i in self.address:
            binCode.append(entry[i])
        return self.controls.addressing(binCode)

    def _getValue(self, index):
        if index not in self.ram:
            return 0
        else:
            return self.ram[index]

    def train(self, entry, negative=False):
        index = self._addressToIndex(entry)
        if not negative:
            self.controls.increase(entry=entry, ram=self.ram, address=self.address, index=index)
        else:
            self.controls.decay(entry=entry, ram=self.ram, address=self.address, index=index)

    def classify(self, entry):
        index = self._addressToIndex(entry)
        return self._getValue(index)
