pipeline {
    agent any

    stages {
        stage('Test Python') {
            steps {
                // Use the Python available on PATH or an agent tool; avoids hardcoded user paths
                bat "%PYTHON% --version"
            }
        }

        stage('Install') {
            steps {
                bat "if not exist reports mkdir reports"
                bat "%PYTHON% -m pip install --upgrade pip"
                bat "%PYTHON% -m pip install -r requirements.txt"
            }
        }

        stage('Test App') {
            steps {
                // Run pytest and emit JUnit XML for Jenkins reporting
                bat "%PYTHON% -m pytest test_app.py -v --junitxml=reports/junit.xml"
            }
        }
    }

    post {
        success {
            echo 'BUILD SUCCESS!'
        }
    }
}
