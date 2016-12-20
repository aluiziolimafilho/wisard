
class BinarizationDefault:

    def __init__(self, cut=0):
        self.cut = cut

    def __call__(self, entry):
        for i,e in enumerate(entry):
            entry[i] = 1 if e > self.cut else 0
        return entry
