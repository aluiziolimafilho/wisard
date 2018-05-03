import random

class BaseLayer:

    def __init__(self):
        pass

    def train(self, entry, aclass):
        self._train(entry, aclass)

    def classify(self, entry, aclass=None):
        return self._classify(entry)

    def _train(self, entry, aclass):
        pass

    def _classify(self, entry):
        pass
