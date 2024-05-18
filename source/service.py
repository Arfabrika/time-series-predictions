from source.session import Session
from fastapi import FastAPI, UploadFile, File, Form, Body
import pandas as pd

app = FastAPI()

# origins = [
#     "http://localhost:3000",
#     "localhost:3000"
# ]


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"]
# )

@app.post("/api/getInitData")
async def getInitData(data: UploadFile,
    needAvg = Form(...),
    learn_size = Form(...),
    needAutoChoice = Form(...),
    ):
    with open('./tmp/data.csv', "wb") as f:
        f.write(data.file.read())
    df = pd.read_csv('./tmp/data.csv')
    session = Session(df, float(learn_size), 
                     needAvg = bool(needAvg),
                     needAutoChoice = bool(needAutoChoice))
    pass
    # result = session.makePrediction(algos)
    # return result
