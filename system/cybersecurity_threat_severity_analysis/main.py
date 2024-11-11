from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
import pickle
import json
from pydantic import BaseModel
from model.lr import evalLRModel  # Make sure evalLRModel is imported here
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Replace with your frontend's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model and feature dictionary
lr_model = None
train_ngram_dict = None

# Load model and feature dictionary at startup
@app.on_event("startup")
def load_model():
    global lr_model, train_ngram_dict
    try:
        # Load the logistic regression model for severity classification
        with open('./trained_model/severity_lr_model.pkl', 'rb') as f:
            lr_model = pickle.load(f)
        # Load the n-gram dictionary used for feature extraction
        with open('./trained_model/severity_train_ngram_dict.json', 'r') as f:
            train_ngram_dict = json.load(f)
    except FileNotFoundError as e:
        print(f"Error loading model or dictionary: {e}")
        raise RuntimeError("Model or dictionary file not found.")

# Pydantic model for request validation
class EvaluationRequest(BaseModel):
    classifier_mode: str
    window_size_list: Optional[List[int]] = [2, 3, 4]
    ngram_extract_mode: str = 'all'
    eval_data: List[dict]

# Endpoint for evaluation
@app.post("/evaluate")
async def evaluate_model(request: EvaluationRequest):
    global lr_model, train_ngram_dict

    # Check if the model and dictionary are loaded
    if lr_model is None or train_ngram_dict is None:
        raise HTTPException(status_code=500, detail="Model or dictionary not loaded")

    # Ensure the classifier mode is valid
    if request.classifier_mode not in ['existence', 'severity']:
        raise HTTPException(status_code=400, detail="Invalid classifier mode")

    # Evaluate model based on classifier mode
    eval_prob = evalLRModel(
        request.window_size_list,
        request.eval_data,
        train_ngram_dict,
        request.ngram_extract_mode,
        lr_model
    )

    # Append scores to each line in eval_data
    for idx, each_line in enumerate(request.eval_data):
        if request.classifier_mode == 'existence':
            each_line['existence_prob'] = eval_prob[idx][1]
        elif request.classifier_mode == 'severity':
            each_line['severity_prob'] = eval_prob[idx][1]

    # Return evaluation results as JSON response
    return JSONResponse(content={"evaluation_results": request.eval_data})

