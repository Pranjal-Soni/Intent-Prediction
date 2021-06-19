"""Fastapi App

This script allows us to create Fast API app to load 
Homepage of our intent prediction app

There are 2 API's in this app

The file consists 2 important functions 
    * home- Load the front end of the app
    * predict- It gives the intent prediction for user's text 
"""

from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
import joblib
import logging
import config
import string
import uvicorn
import pandas as pd
from sklearn.svm import SVC
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import time


logging.basicConfig(filename=config.LOGS_DIR,level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

#punctuations
punc = string.punctuation
#load the vectorizer
vectorizer = joblib.load(config.VECTORIZER_PATH)
logging.info("Vectorizer loaded Successfully")


#load the model
svc_classifier = joblib.load(config.MODEL_PATH)
logging.info("Model loaded Successfully")

#html file templates
templates = Jinja2Templates(directory=config.TEMPLATES_DIR)

### initialise application
app = FastAPI()

@app.get("/")
def home(request: Request):
    """Load Home page of the application"""
    return templates.TemplateResponse("index.html", {"request": request})

#variable to keep record of requests
request_id  = 0

@app.post("/predict_intent")    
async def predict(text:str):
    """Preprocess the text and make prediction for the text input"""
    
    global request_id
    request_id += 1

    #preprocess text
    input = ''.join([char for char in text if char not in punc]).lower()
    input = pd.DataFrame.sparse.from_spmatrix(vectorizer.transform([input]))

    #model prediction
    prediction = svc_classifier.predict(input.values)
    

    if prediction[0] == 0: result =  {"id":request_id,"intent":"FindConnection"}
    else: result =  {"id":request_id,"intent":"DepartureTime"}

    logging.info(f"Request ID : {request_id} TEXT : {text} INTENT : {result['intent']}")
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)