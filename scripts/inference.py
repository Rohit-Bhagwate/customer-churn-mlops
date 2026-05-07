import joblib
import pandas as pd
import json
import os


def model_fn(model_dir):
    model_path = os.path.join(model_dir, "model.joblib")
    return joblib.load(model_path)

def input_fn(request_body, request_content_type):
    if request_content_type == "application/json":
        data = json.loads(request_body)
        return pd.DataFrame([data])

    raise Exception("Unsupported content type")


def predict_fn(input_data, model):
    preds = model.predict(input_data)
    return preds


def output_fn(prediction, content_type):
    return json.dumps(prediction.tolist())