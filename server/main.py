from source.client import makeData, makeAlgoData
from source.service import Session
from source.algorithms.algos import Algos
import uvicorn

def mainfunc():
    learnSize = 0.7
#     # inputData = makeData("./datasets/covid_clear.csv", "ill_cnt", False)
    inputData = makeData("./datasets/metro.csv", "Traffic_volume")
    session = Session(inputData, learnSize)

    # algo = Algos(session.learn_size, 'X', 'Y')
    # algo.linearRegression(inputData, params = [3])
    # algo.movingAverage(inputData, 8, algo.linearRegression, [3], 'move')
    # algo.outtbl.save()

    data = makeAlgoData()

    result = session.makePrediction(data)
    print(result)
    # for el in result:
    #     print(el['metrics'])
    # try:
    #     print(result[0]["smetrics"])
    # except:
    #     print(result)

# if __name__ == '__main__':
#     mainfunc()
if __name__ == "__main__":
    uvicorn.run("source.service:app", host="0.0.0.0", port=8000, reload=True)