import tarfile
import os

model_path = 'src/model/model.joblib'
tar_path = 'model.tar.gz'

with tarfile.open(tar_path, "w:gz") as tar:
    tar.add(model_path,arcname='model.joblib')

print("model.tar.gz created")