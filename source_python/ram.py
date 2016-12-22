from random import randint

class CompactedRAM:

    def __init__(self):
        self.ram = {}

    def __contains__(self, index):
        return index in self.ram

    def __getitem__(self, index):
        if index in self.ram:
            return self.ram[index]
        return 0

    def __setitem__(self, index, item):
        if item == 0:
            del self.ram[index]
        else:
            self.ram[index] = item

class AddressControl:

    def __init__(self, addressSize, entrySize, addressing):
        self.addressing = addressing
        self.address = [ randint(0, entrySize-1) for x in range(addressSize) ]

    def __getitem__(self, entry):
        binCode = []
        for i in self.address:
            binCode.append(entry[i])
        return self.addressing(binCode)

class RAM:

    def __init__(self, addressSize, entrySize, controls):
        self.controls = controls
        self.ram = CompactedRAM()
        self.address = AddressControl(addressSize, entrySize, controls.addressing)

    def train(self, entry, negative=False):
        index = self.address[entry]
        if not negative:
            self.controls.increase(entry=entry, ram=self.ram, address=self.address, index=index)
        else:
            self.controls.decay(entry=entry, ram=self.ram, address=self.address, index=index)

    def classify(self, entry):
        index = self.address[entry]
        return self.ram[index]
