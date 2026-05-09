pipeline {
    agent any

    environment {
        FUNCTION_NAME = 'url-shortener'
        REGION        = 'eu-north-1'
    }

    stages {
        stage('Install dependencies') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '.venv/bin/python -m pytest tests/ -v'
            }
        }

        stage('Package') {
            steps {
                sh 'zip -j deployment.zip src/*.py'
            }
        }

        stage('Deploy to Lambda') {
            steps {
                sh '''
                    aws lambda update-function-code \
                        --function-name $FUNCTION_NAME \
                        --zip-file fileb://deployment.zip \
                        --region $REGION
                '''
            }
        }
    }

    post {
        success {
            echo 'Deployment successful'
        }
        failure {
            echo 'Pipeline failed — Lambda was not updated'
        }
    }
}