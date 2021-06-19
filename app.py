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
import string
import pandas as pd
from sklearn.svm import SVC
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

import time

#punctuations
punc = string.punctuation
#load the vectorizer
vectorizer = joblib.load("./utils/vectorizer.pkl")

#load the model
svc_classifier = joblib.load("./model/svc_classifier.pkl")

#html file templates
templates = Jinja2Templates(directory="./templates/")

### initialise application
app = FastAPI(debug=True)

@app.get("/")
def home(request: Request):
    """Load Home page of the application"""
    return templates.TemplateResponse("index.html", {"request": request})

#
request_id  = 0

@app.post("/predict_intent")    
async def predict(text:str):
    """Preprocess the text and make prediction for the text input"""
    #preprocess text
    input = ''.join([char for char in text if char not in punc]).lower()
    input = pd.DataFrame.sparse.from_spmatrix(vectorizer.transform([input]))

    #model prediction
    prediction = svc_classifier.predict(input.values)
    global request_id
    request_id += 1

    if prediction[0] == 0: return {"id":request_id,"intent":"FindConnection"}
    else: return {"id":request_id,"intent":"DepartureTime"}

