
class BinarizationDefault:

    def __init__(self, cut=0):
        self.cut = cut

    def __call__(self, entry):
        for i,e in enumerate(entry):
            entry[i] = 1 if e > self.cut else 0
        return entry

class BinarizationAverage:

    def __call__(self, entry):
        average = float(sum(entry))/len(entry)
        cut = lambda x: 1 if x > average else 0
        return list(map(cut,entry))
