import matplotlib.pyplot as plt
import csv
import random

TEST = "dota2Test.csv"
TRAIN = "dota2Train.csv"

class datapoint:
    def __init__(self, outcome, mode, heroes):
        self.outcome = outcome
        self.mode = mode
        self.heroes = heroes

class perceptron:
    def __init__(self, wsize):
        self.weights = []
        i = 0
        while i < wsize:
            self.weights.append(0)
            i += 1
        self.bias = 0

def read_input():
    traindata = []
    testdata = []
    with open(TRAIN, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            i = 4
            theros = []
            while i < len(row):
                theros.append(int(row[i]))
                i += 1
            temp = datapoint(int(row[0]), int(row[2]), theros)
            traindata.append(temp)
    with open(TEST, "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            i = 4
            theros = []
            while i < len(row):
                theros.append(int(row[i]))
                i += 1
            temp = datapoint(int(row[0]), int(row[2]), theros)
            testdata.append(temp)
    return (traindata, testdata)
def predict(ptron, trainvals):
    i = 0
    activation = 0
    while i < len(ptron.weights):
        activation += ptron.weights[i]*trainvals.heroes[i]
        i += 1
    activation += ptron.bias
    if activation <= 0:
        activation = -1
    else:
        activation = 1
    return activation

def update(ptron, trueval, trainvals, learnrate):
    i = 0
    while i < len(ptron.weights):
        ptron.weights[i] += learnrate * trueval * trainvals.heroes[i]
        i += 1
    ptron.bias += trueval

def sortMode(data, mode):
    temp = []
    for point in data:
        if point.mode == mode:
            temp.append(point)
    return temp

def K_Fold(K, data):
    tdata = data.copy()
    folds = {}
    for i in range(K):
        folds[i] = []
    while len(tdata) >= K:
        for i in range(K):
            val = random.randrange(len(tdata))
            folds[i].append(tdata[val])
            tdata.pop(val)
    if len(tdata) != 0:
        for i in range(len(tdata)):
            val = random.randrange(len(tdata))
            folds[i].append(tdata[val])
            tdata.pop(val)
    return folds

#sort data function????

def main():
    traind, testd = read_input()
    dotguess = perceptron(len(traind[0].heroes))
    learnrate = 0.5
    traind_mode = {}
    X = []
    Y = []
    errs = []
    n = 0
    p = 0
    fp = 0
    fn = 0
    tp = 0
    tn = 0
    #how many iterations?
    i = 1
    for i in range(10):
        traind_mode[i] = sortMode(traind, i)
    for j in range(20):
        folded = K_Fold(10, traind_mode[2])
        err2 = []
        for i in range(10):
            errorcount = 0
            test = folded[i]
            train = []
            for k in range(10):
                if k != i:
                    train += folded[k]
            for point in train:
                a = predict(dotguess, point)
                if a*point.outcome <= 0:
                    update(dotguess, point.outcome, point, learnrate)
            for point in test:
                a = predict(dotguess, point)
                if a == -1:
                    n += 1
                else:
                    p += 1
                if a*point.outcome > 0:
                    if a == -1:
                        tn += 1
                    else:
                        tp += 1
                else:
                    errorcount += 1
                    if a == -1:
                        fn += 1
                    else:
                        fp += 1
            errs.append(errorcount)
            err2.append(errorcount)
            print(dotguess.weights)
            print(dotguess.bias)
        X.append(j)
        avg = sum(err2)/10
        Y.append(1-(avg/len(test)))
    print(errs)
    avgerr = sum(errs)/20
    print(X)
    print(Y)
    plt.plot(X, Y)
    plt.xlabel('Epochs')
    plt.ylabel('Accuracy')
    plt.title('Dota 2 Perceptron Accuracy')
    plt.show()
    print(avgerr)
    print("Accuracy:", 1-((avgerr)/len(test)))
    print("Precision:", tp/p)
    print("Recall:", tp/(tp+fn))
    #for point in test:
        #a = predict(dotguess, point)
        #predict
        #if true, nothing
        #else, update
    #test perceptron on test points

if __name__ == '__main__':
    main()