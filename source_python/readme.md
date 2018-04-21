# To use just do:

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

# Getting mental images:


    classes = wsd.getMentalImages()

    for aClass in classes:
        print("class: "+str(aClass)+" mental image: "+str(classes[aClass]))

# Parameters specification:

    below we show the default values of each parameter:

    wsd = Wisard(
              addressSize = 3,
              bleachingActivated = True,
              seed = random.randint(0, 1000000),
              verbose = None,
              makeBleaching = None,
              ramcontrols = None
              )

    addressSize -- int -- the size of addressing to the ram
    bleachingActivated -- boolean -- use bleaching or not in the classification
    seed -- int -- the seed used to generate the mapping of indexes to the rams
    verbose -- function -- you can make your own verbose function of the training and classification processes
    makeBleaching -- function -- you can customize your own classification algorithm
    ramcontrols -- function -- ignore that for while, because it is in development

# Format of verbose function:

  def verbose(fase=None, index=None, total=None, end=None):
    # do the print on your format.
    print("fase: "+fase+" step:"+index)

  fase -- string -- show 'training' in the training process and show 'classifying' in the classifying process
  index -- int -- show the step of the process
  total -- int -- show the total steps of the process
  end -- boolean -- become true in the end of the process

# Format of bleaching function:

class YourBleancingFunction:

    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, discriminatorsoutput):
      # do some algorithm of classification
      return discriminatorsoutput

discriminatorsoutput -- dict -- it is a dictionary that the key is the class of the classification problem and the value is the discriminator output.
discriminatoroutput -- list(2) -- the first value is the list of the outputs of rams,
                  the second value is the importance of the discriminator between all others,
                  this value will be used to choose the class of the entry.
return -- dict -- the same format of discriminatorsoutput

to use just pass the class as parameter to the Wisard.

# Binarization functions:

there is some functions in the file binarization.py, to you use to binarize the entry.
exemple of use:
      bin = BinarizationDefault(cut=1)

      X = [
          [1,2,3,0,0,0,0,0],
          [1,7,5,1,0,0,0,0],
          [0,0,0,0,1,4,1,8],
          [0,0,0,0,0,1,6,3]
      ]

      for i,entry in enumerate(X):
        X[i] = bin(entry)
