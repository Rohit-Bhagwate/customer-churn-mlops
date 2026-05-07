import pandas as pd

def validate_data(df: pd.DataFrame):
    #check empty
    if df.empty:
        raise ValueError("Dataset is Empty")

    #check missing values
    if df.isnull().sum().sum() > 0:
        raise ValueError("Dataset Contains Missing Values")

    print("Dataset Validation Passed")
    return True