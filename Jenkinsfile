pipeline {
    agent any
    environment {
        PYTHONUNBUFFERED = '1'
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Install dependencies') {
            steps {
                sh 'pip install --upgrade pip'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                    sh 'pytest test_app.py --maxfail=1 --disable-warnings'
            }
        }
        stage('Build Docker image') {
            steps {
                sh 'docker build -t fastapi-todo .' 
            }
        }
        stage('Run Docker container') {
            steps {
                sh 'docker run -d -p 8000:8000 --name fastapi-todo fastapi-todo'
            }
        }
    }
    post {
        always {
            sh 'docker rm -f fastapi-todo || true'
        }
    }
}
