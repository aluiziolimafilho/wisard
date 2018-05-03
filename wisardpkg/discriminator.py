import random
from .ram import RAM

class Discriminator:

    def __init__(self, name, entrySize, addressSize, ramcontrols):
        self.name = name
        self.entrySize = entrySize
        numberOfRAMS = int(entrySize/addressSize)
        indexes = [i for i in range(entrySize)]
        random.shuffle(indexes)
        self.rams = [ RAM(indexes[x*addressSize:(1+x)*addressSize], ramcontrols) for x in range(numberOfRAMS) ]
        remain = entrySize%addressSize
        if remain > 0:
            newindexes = indexes[:-remain] + [ random.randint(0,entrySize-1) for x in range(addressSize-remain)]
            self.rams.append(RAM(newindexes, ramcontrols))



    def train(self, entry, negative=False):
        for ram in self.rams:
            ram.train(entry, negative)

    def classify(self, entry):
        return [ ram.classify(entry) for ram in self.rams ]

    def getMentalImage(self):
        mentalImage = [0 for x in range(self.entrySize)]
        for ram in self.rams:
            for mentalPixel in ram.getMentalImage():
                mentalImage[mentalPixel[0]]=mentalPixel[1]
        return mentalImage
