import pandas as pd
import os
from src.data.validation import  validate_data
from src.data.train import train_model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def run_pipeline():
    data_path = os.path.join(BASE_DIR, "data","WA_Fn-UseC_-Telco-Customer-Churn.csv")

    #Load Data
    df = pd.read_csv(data_path)

    #Step 1: Validation
    validate_data(df)

    #Step 2: Training + S3 upload
    train_model(data_path)

    print("Pipeline completed successfully!")

if __name__ == "__main__":
    run_pipeline()

