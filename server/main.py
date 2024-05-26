from source.client import makeData, makeAlgoData
from source.service import Session
import uvicorn

def mainfunc():
    learnSize = 0.7
    inputData = makeData("./datasets/metro.csv", "Traffic_volume")
    session = Session(inputData, learnSize)
    data = makeAlgoData()
    result = session.makePrediction(data)
    print(result)

IS_DEBUG = False

if __name__ == '__main__' and IS_DEBUG:
    mainfunc()
if __name__ == "__main__" and not IS_DEBUG:
    uvicorn.run("source.service:app", host="0.0.0.0", port=8000, reload=True)