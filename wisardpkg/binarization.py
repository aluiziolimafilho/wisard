import math

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

class Quarterization:

    def code(self, x, mean, dp):
        if x > mean+dp:
            return 3
        elif x > mean:
            return 2
        elif x > (mean-dp):
            return 1
        else:
            return 0

    def __call__(self, entry):
        average = float(sum(entry))/len(entry)
        dp = 0
        for x in entry:
            dp += (x - average)**2
        dp = (dp/len(entry))**0.5

        for i in xrange(len(entry)):
            entry[i] = self.code(entry[i], average, dp)
        return entry

class Customrization:

    def __init__(self, base=2):
        self.base=base-1

    def code(self, x, mean, dp):
        if dp == 0:
            dp = 1
        out = (((x - mean)/dp) + 1.0)/2.0
        if out > 1 or out < -1:
            return self.base
        elif out < 0:
            return round(-self.base*out)
        else:
            return round(self.base*out)

    def __call__(self, entry):
        average = float(sum(entry))/len(entry)
        dp = 0
        for x in entry:
            dp += math.pow(x - average, 2)
        dp = math.sqrt(dp/len(entry))

        for i in xrange(len(entry)):
            entry[i] = self.code(entry[i], average, dp)
        return entry
