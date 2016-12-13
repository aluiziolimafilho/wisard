from ram import RAM

class Discriminator:

    def __init__(self, name, entrySize, addressSize, addressing, numberOfRAMS=None):
        if numberOfRAMS is None:
            numberOfRAMS = int(entrySize/addressSize)
        self.rams = [ RAM(addressSize, entrySize, addressing) for x in range(numberOfRAMS) ]

    def train(self, entry):
        for ram in self.rams:
            ram.train(entry)

    def classify(self, entry):
        return [ ram.classify(entry) for ram in self.rams ]
