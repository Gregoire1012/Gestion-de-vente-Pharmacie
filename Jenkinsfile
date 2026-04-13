pipeline {
    agent any

    stages {

        stage('Clone GitHub') {
            steps {
                git branch: 'main', url: 'https://github.com/Gregoire1012/Gestion-de-vente-Pharmacie.git'
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                python3 -m venv venv
                source venv/bin/activate
                pip install --upgrade pip
                pip install django
                '''
            }
        }

        stage('Migrations') {
            steps {
                sh '''
                source venv/bin/activate
                python manage.py migrate
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                source venv/bin/activate
                python manage.py check
                '''
            }
        }

        stage('Run Server (Test Only)') {
            steps {
                echo "Build OK - Ready for deploy"
            }
        }
    }
}
