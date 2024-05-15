pipeline {
    agent {
        docker { image 'python:3.12' }
    }
     environment {
        HELLO_WORLD = 'true'
        DB_ENGINE = 'sqlite'
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from the Git repository
                git 'git@github.com:walidsa3d/anyq.git'
            }
        stage('Build') {
            steps {
                sh 'pip install poetry'
                sh 'poetry install'
            }
        }
        stage('Test') {
            steps {
                sh 'pytest -v'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}
post {
        always {
           echo 'Finished'
            deleteDir() // Clean the workspace
        }
        success {
           echo 'I succeeded!'
        }
        unstable {
            echo 'I am unstable :/'
        }
        failure {
            echo 'I failed :('
        }
        changed {
            echo 'Latest job status differs from previous job status'
        }
}
}