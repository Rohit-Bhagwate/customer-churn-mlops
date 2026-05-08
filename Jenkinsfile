pipeline {
    agent any

    environment {
        AWS_REGION = "ap-south-1"
        ECR_REPO = "232932848445.dkr.ecr.ap-south-1.amazonaws.com/churn-api"
        IMAGE_TAG = "latest"
    }

    stages {

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Train Model') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-credentials'
                ]]) {
                    sh '''
                    . venv/bin/activate
                    python3 -m src.pipeline.pipeline
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t churn-api .
                '''
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region $AWS_REGION | \
                docker login --username AWS --password-stdin $ECR_REPO
                '''
            }
        }

        stage('Tag Image') {
            steps {
                sh '''
                docker tag churn-api:latest $ECR_REPO:$IMAGE_TAG
                '''
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                docker push $ECR_REPO:$IMAGE_TAG
                '''
            }
        }

        stage('Deploy to EC2') {
            steps {
                sh '''
                ssh -o StrictHostKeyChecking=no ubuntu@YOUR_EC2_IP << 'EOF'
                    docker pull 232932848445.dkr.ecr.ap-south-1.amazonaws.com/churn-api:latest
                    docker stop churn || true
                    docker rm churn || true
                    docker run -d -p 5000:5000 --name churn 232932848445.dkr.ecr.ap-south-1.amazonaws.com/churn-api:latest
                EOF
                '''
            }
        }
    }

    post {
        success {
            echo "CI/CD Pipeline Completed Successfully!"
        }
        failure {
            echo "Pipeline Failed!"
        }
    }
}