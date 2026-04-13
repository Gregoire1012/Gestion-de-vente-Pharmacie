pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                git branch: 'main', url: 'https://github.com/Gregoire1012/Gestion-de-vente-Pharmacie.git'
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                python3 -m venv venv
                ./venv/bin/pip install --upgrade pip
                ./venv/bin/pip install django
                '''
            }
        }

        stage('Migrations') {
            steps {
                sh '''
                ./venv/bin/python manage.py migrate
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                ./venv/bin/python manage.py check
                '''
            }
        }

        stage('Done') {
            steps {
                echo "SUCCESS 🚀"
            }
        }
    }
}
