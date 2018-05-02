from discriminator import Discriminator

class Cluster():

    def __init__(self, **kwargs):
        self.entrySize=kwargs.get('entrySize')
        self.addressSize=kwargs.get('addressSize')
        self.ramcontrols=kwargs.get('ramcontrols')
        self.minScore = kwargs.get('minScore',2)
        self.threshold = kwargs.get('threshold', 5)
        self.discriminators = []

    def _createDiscriminator(self):
        return Discriminator('clus', self.entrySize, self.addressSize, self.ramcontrols)

    def score(self, discriminatoroutput):
        m = max(discriminatoroutput)
        return sum(discriminatoroutput)/(len(discriminatoroutput)*float(m))

    def train(self, entry):
        newDiscriminator = True
        for d in self.discriminators:
            output = d.classify(entry)
            if self.score(output) >= min(1, self.minScore + max(output)/float(self.threshold)):
                d.train(entry)
                newDiscriminator = False

        if newDiscriminator:
            d = self._createDiscriminator()
            self.discriminators.append(d)
            d.train(entry)

    def classify(self, entry):
        output = []
        for d in self.discriminators:
            output.append(d.classify(entry))
        return output

    def getMentalImages(self):
        images = []
        for d in self.discriminators:
            images.append(d.getMentalImage())
        return images
