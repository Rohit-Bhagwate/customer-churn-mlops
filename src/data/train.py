import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import joblib
import mlflow
import mlflow.sklearn
import os
import boto3

def train_model(data_path):
    # MLflow setup
    mlflow.set_experiment("churn_simple")

    # Load data
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(BASE_DIR, "data", "WA_Fn-UseC_-Telco-Customer-Churn.csv")

    df = pd.read_csv(data_path)

    # Cleaning
    df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors='coerce')
    df = df.drop("customerID", axis=1)
    df["Churn"] = df["Churn"].map({"Yes": 1, "No": 0})
    df = df.dropna()

    # Split
    X = df.drop("Churn", axis=1)
    y = df["Churn"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Preprocessing
    cat_cols = X.select_dtypes(include=['object']).columns
    num_cols = X.select_dtypes(exclude=['object']).columns

    preprocessor = ColumnTransformer([
        ("num", StandardScaler(), num_cols),
        ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols)
    ])

    # Pipeline
    pipeline = Pipeline([
        ("prep", preprocessor),
        ("model", LogisticRegression(max_iter=1000))
    ])

    # MLflow run
    with mlflow.start_run():

        pipeline.fit(X_train, y_train)

        preds = pipeline.predict(X_test)
        acc = accuracy_score(y_test, preds)

        print("Accuracy:", acc)

        mlflow.log_metric("accuracy", acc)

        # Save model locally
        model_dir = os.path.join(BASE_DIR, "model")
        os.makedirs(model_dir, exist_ok=True)

        model_path = os.path.join(model_dir, "model.joblib")
        joblib.dump(pipeline, model_path)

        print("✅ Model saved at:", model_path)

        s3 = boto3.client("s3")

        bucket_name = 'churn-project-bucker-rohit1'

        #--------------
        #Upload to S3
        #--------------
        s3.upload_file(
            model_path,
            bucket_name,
            "model/model.joblib"
        )

        print("Model uploaded to S3")
    return model_path
