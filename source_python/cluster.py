from discriminator import Discriminator

class Cluster():

    def __init__(self, **kwargs):
        self.entrySize=kwargs.get('entrySize')
        self.addressSize=kwargs.get('addressSize')
        self.ramcontrols=kwargs.get('ramcontrols')
        self.discriminators = []

    def _createDiscriminator(self):
        return Discriminator('clus', self.entrySize, self.addressSize, self.ramcontrols)

    def train(self, entry):
        pass

    def classify(self, entry):
        pass
