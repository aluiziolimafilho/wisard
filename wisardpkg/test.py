from .wisard import Wisard
from .cluswisard import ClusWisard

# Entry example

X = [
    [1,1,1,0,0,0,0,0],
    [1,1,1,1,0,0,0,0],
    [0,0,0,0,1,1,1,1],
    [0,0,0,0,0,1,1,1]
]

y = [
    "cold",
    "cold",
    "hot",
    "hot"
]

# Test with Wisard
print("\n### Test with Wisard ###\n")

wsd = Wisard(addressSize=4, bleachingActivated=True)

wsd.trainall(X, y)
out = wsd.classifyall(X)

for i in range(len(y)):
    print("o: "+y[i]+" p: "+out[i])


print("\n### Get Mental Images ###\n")

classes = wsd.getMentalImages()

for aClass in classes:
    print("class: "+str(aClass)+" mental image: "+str(classes[aClass]))

# Test with ClusWisard
print("\n### Test with ClusWisard ###\n")

clus = ClusWisard(addressSize=4)

clus.trainall(X, y)
out = clus.classifyall(X)

for i in range(len(y)):
    print("o: "+y[i]+" p: "+out[i])
