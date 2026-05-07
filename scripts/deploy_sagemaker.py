import sagemaker
from sagemaker.sklearn.model import SKLearnModel

role = "arn:aws:iam::232932848445:role/service-role/AmazonSageMaker-ExecutionRole-20260504T141657"

model = SKLearnModel(
    model_data = "s3://churn-project-bucker-rohit1/model/model.tar.gz",
    role = role,
    entry_point = "inference.py",
    source_dir="scripts",
    framework_version = "1.2-1"
)

predictor = model.deploy(
    instance_type="ml.t2.medium",
    initial_instance_count=1
)

print("EndPoint deployed")
print(predictor.endpoint_name)
