from fastapi import FastAPI, File, Form
import pandas as pd
from source.session import Session
import json

app = FastAPI()

@app.post("/api/predict")
async def predict(
    data: bytes = File(...),
    needAvg: bool = Form(...),
    learn_size: float = Form(...),
    needAutoChoice: bool = Form(...),
    algos_str: str = Form(...)
):
    with open('./tmp/data.csv', "wb") as f:
        f.write(data)
    df = pd.read_csv('./tmp/data.csv')
    df["Date"] = pd.to_datetime(df["Date"], format='%Y-%m-%d')
    algos = json.loads(algos_str)
    session = Session(df[["Date", df.columns[-1]]], float(learn_size), 
                     needAvg = bool(needAvg),
                     needAutoChoice = bool(needAutoChoice))
    result = session.makePrediction({"algos": algos})
    return result
