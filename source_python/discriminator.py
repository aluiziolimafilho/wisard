from ram import RAM

class Discriminator:

    def __init__(self, name, entrySize, addressSize, ramcontrols, numberOfRAMS=None):
        self.name = name
        if numberOfRAMS is None:
            numberOfRAMS = int(entrySize/addressSize)
        self.rams = [ RAM(addressSize, entrySize, ramcontrols) for x in range(numberOfRAMS) ]

    def train(self, entry, negative=False):
        for ram in self.rams:
            ram.train(entry, negative)

    def classify(self, entry):
        return [ ram.classify(entry) for ram in self.rams ]

class DeepDiscriminator:

    def __init__(self, name, entrySize, addressSize, ramcontrols, numberOfDiscriminators=10, numberOfRAMS=None, discriminatorBleaching=None):
        self.name = name
        self.discriminatorBleaching = discriminatorBleaching
        self.discriminators = []
        for x in xrange(0,numberOfDiscriminators):
            discriminator = Discriminator(name, entrySize, addressSize, ramcontrols, numberOfRAMS)
            self.discriminators.append(discriminator)

    def train(self, entry, negative=False):
        for discriminator in self.discriminators:
            discriminator.train(entry, negative)

    def classify(self, entry):
        out = []
        for d in self.discriminators:
            out += d.classify(entry)
        return out
