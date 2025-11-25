pipeline {
    agent any
    
    stages {
        stage('Install dependencies') {
            steps {
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
                sh 'docker stop fastapi-todo || exit 0'
                sh 'docker rm fastapi-todo || exit 0'
                sh 'docker run -d -p 8000:8000 --name fastapi-todo fastapi-todo'
            }
        }
    }
    
    post {
        success {
            echo 'Build réussi! App disponible sur http://localhost:8000'
        }
        failure {
            echo 'Build échoué!'
        }
    }
}