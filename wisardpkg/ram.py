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
            if index in self.ram:
                del self.ram[index]
        else:
            self.ram[index] = item

    def __len__(self):
        return len(self.ram)

class AddressControl:

    def __init__(self, indexes, addressing):
        self.addressing = addressing
        self.indexes = indexes

    def __getitem__(self, entry):
        binCode = []
        for i in self.indexes:
            binCode.append(entry[i])
        return self.addressing(binCode)

    def __len__(self):
        return len(self.indexes)

class RAM:

    def __init__(self, indexes, controls):
        self.controls = controls
        self.ram = CompactedRAM()
        self.address = AddressControl(indexes, controls.addressing)

    def train(self, entry, negative=False):
        index = self.address[entry]
        if not negative:
            self.controls.increase(entry=entry, ram=self.ram, address=self.address, index=index)
        else:
            self.controls.decay(entry=entry, ram=self.ram, address=self.address, index=index)

    def classify(self, entry):
        index = self.address[entry]
        return self.ram[index]

    def getMentalImage(self):
        mental = [ [x,0] for x in self.address.indexes]
        for address in self.ram.ram:
            if address == 0:
                continue
            for i in range(len(self.address)):
                if (address & 2**i) > 0:
                    mental[i][1] += self.ram[address]
        return mental
