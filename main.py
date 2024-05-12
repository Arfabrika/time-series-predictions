from source.client import makeData, makeAlgoData
from source.service import Session

def mainfunc():
    learnSize = 0.7
    inputData = makeData("./datasets/metro.csv", "Traffic_volume")
    session = Session(inputData, learnSize)

    algos = makeAlgoData()

    result = session.makePrediction(algos)
    # try:
    #     print(result[0]["metrics"])
    # except:
    # print(result)
    for el in result:
        print(el['metrics'])

if __name__ == '__main__':
    mainfunc()