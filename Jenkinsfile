pipeline {
    agent any
    
    stages {
        stage('Test Python') {
            steps {
                bat 'python --version'
            }
        }
        
        stage('Setup Environment') {
            steps {
                echo 'Setting up Python virtual environment...'
                bat '''
                    if exist venv rmdir /s /q venv
                    python -m venv venv
                '''
            }
        }
        
        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies...'
                bat '''
                    call venv\\Scripts\\activate.bat
                    python -m pip install --upgrade pip
                    pip install fastapi uvicorn pytest sqlalchemy pydantic httpx
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                echo 'Running pytest tests...'
                bat '''
                    call venv\\Scripts\\activate.bat
                    pytest -v
                '''
            }
        }
        
        stage('Health Check') {
            steps {
                echo 'Verifying application...'
                bat '''
                    call venv\\Scripts\\activate.bat
                    python -c "from app.main import app; print('App imported successfully')"
                '''
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs above.'
        }
        always {
            echo 'Cleaning up workspace...'
        }
    }
}