from wisard import Wisard

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

wsd = Wisard(addressSize=4, bleachingActivated=True)

print("seed: "+str(wsd.seed))

wsd.trainall(X, y)

out = wsd.classifyall(X)

for i in range(len(y)):
    print("o: "+y[i]+" p: "+out[i])

classes = wsd.getMentalImages()

for aClass in classes:
    print("class: "+str(aClass)+" mental image: "+str(classes[aClass]))
