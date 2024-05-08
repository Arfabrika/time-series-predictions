from source.client import makeData, makeAlgoData
from source.service import Session

def mainfunc():
    learnSize = 0.7
    inputData = makeData("./datasets/programming languages.csv", "Rust", True)
    #inputData = makeData("./datasets/covid_clear.csv", "ill_cnt", False)
    session = Session(inputData, learnSize)

    algos = makeAlgoData()

    result = session.makePrediction(algos)
    print(result)

if __name__ == '__main__':
    mainfunc()