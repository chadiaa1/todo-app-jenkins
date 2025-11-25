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
                bat 'pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                bat 'pytest test_app.py --maxfail=1 --disable-warnings'
            }
        }
        stage('Build Docker image') {
            steps {
                bat 'docker build -t fastapi-todo .' 
            }
        }
        stage('Run Docker container') {
            steps {
                bat 'docker run -d -p 8000:8000 --name fastapi-todo fastapi-todo'
            }
        }
    }
    post {
        always {
            bat 'docker rm -f fastapi-todo || exit 0'
        }
    }
}