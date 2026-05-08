pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'
    }

    stages {

        stage('Install Dependencies') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate

                pip install --upgrade pip
                pip install -r requirements.txt

                pip install "sagemaker<3"
                pip install awscli
                '''
            }
        }

        stage('Run Training Pipeline') {
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

        stage('Create model.tar.gz') {
            steps {
                sh '''
                cd src/model

                tar -czf model.tar.gz model.joblib
                '''
            }
        }

        stage('Upload Model To S3') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-credentials'
                ]]) {

                    sh '''
                    . venv/bin/activate

                    aws s3 cp src/model/model.tar.gz s3://churn-project-bucker-rohit1/model/model.tar.gz
                    '''
                }
            }
        }

        stage('Deploy To SageMaker') {
            steps {
                withCredentials([[
                    $class: 'AmazonWebServicesCredentialsBinding',
                    credentialsId: 'aws-credentials'
                ]]) {

                    sh '''
                    . venv/bin/activate

                    python3 scripts/deploy_sagemaker.py
                    '''
                }
            }
        }
    }

    post {

        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}