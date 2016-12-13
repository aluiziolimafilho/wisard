# To use just do:

    from wisard import WiSARD

    X = [
        [1,1,1,0,0,0,0,0],
        [1,1,1,1,0,0,0,0],
        [1,1,1,1,1,1,1,0],
        [1,1,1,1,1,1,1,1]
    ]

    y = [
        "cold",
        "cold",
        "hot",
        "hot"
    ]

    wsd = WiSARD(addressSize=3, bleachingActivated=True)

    print("seed: "+str(wsd.seed))

    wsd.train(X, y)

    out = wsd.classify(X)
