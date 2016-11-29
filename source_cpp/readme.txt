# To use just do:

    vector<vector<int>> X = {
        {1,1,1,0,0,0,0,0},
        {1,1,1,1,0,0,0,0},
        {1,1,1,1,1,1,1,0},
        {1,1,1,1,1,1,1,1}
    }

    vector<vector<string>> y = {
        "cold",
        "cold",
        "hot",
        "hot"
    }

    int addressSize = 3;
    bool bleaching = true;
    Wisard wisard(addressSize,bleaching);

    wisard.print();

    wisard.train(X, y);

    vector<string> labels = wisard.classify(X);
