pipeline {
    agent any

    environment {
        VENV_DIR   = 'venv'
        DEPLOY_DIR = 'C:\\JenkinsDeploy\\library-cicd'
    }

    options {
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timeout(time: 15, unit: 'MINUTES')
    }

    triggers {
        pollSCM('H/2 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Setup Python') {
            steps {
                bat 'python --version'
                bat 'python -m venv %VENV_DIR%'
                bat '%VENV_DIR%\\Scripts\\python -m pip install --upgrade pip'
                bat '%VENV_DIR%\\Scripts\\pip install -r requirements.txt'
            }
        }

        stage('Lint') {
            steps {
                bat '%VENV_DIR%\\Scripts\\flake8 --max-line-length=100 --exclude=%VENV_DIR% .'
            }
        }

        stage('Test') {
            steps {
                bat '%VENV_DIR%\\Scripts\\pytest -v --junitxml=reports\\results.xml'
            }
        }

        stage('Build') {
            steps {
                bat 'if not exist dist mkdir dist'
                bat 'powershell -NoProfile -Command "Compress-Archive -Path *.py,templates,requirements.txt -DestinationPath dist\\library-cicd-%BUILD_NUMBER%.zip -Force"'
                archiveArtifacts artifacts: 'dist/*.zip', fingerprint: true
            }
        }

        stage('Deploy') {
            steps {
                bat 'if not exist "%DEPLOY_DIR%" mkdir "%DEPLOY_DIR%"'
                bat 'copy /Y *.py "%DEPLOY_DIR%\\"'
                bat 'copy /Y requirements.txt "%DEPLOY_DIR%\\"'
                bat 'xcopy /E /I /Y templates "%DEPLOY_DIR%\\templates"'
                bat '%VENV_DIR%\\Scripts\\python "%DEPLOY_DIR%\\smoke_check.py"'
            }
        }
    }

    post {
        always {
            junit allowEmptyResults: true, testResults: 'reports/results.xml'
        }
        success {
            echo 'Pipeline success: tests passed and deployed'
        }
        failure {
            echo 'Pipeline failed: check Console Output'
        }
    }
}
