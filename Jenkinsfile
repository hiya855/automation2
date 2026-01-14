pipeline {
    agent any

    environment {
        // ID must match the Credential ID you create in Jenkins
        DOCKER_HUB_CRED = credentials('dcker-hub-id')
        IMAGE_NAME = "hiya855/automation"
        DOCKER_API_VERSION = "1.44"
    }

    stages {
        stage('Checkout') {
            steps {
                // Jenkins pulls the latest code from your repo
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                // Builds using the multi-stage Dockerfile we created
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest ."
            }
        }

        stage('Security Scan (Trivy)') {
            steps {
                // Scans for vulnerabilities before pushing
                sh "trivy image --severity HIGH,CRITICAL --docker-host unix:///var/run/docker.sock ${IMAGE_NAME}:latest"
            }
        }

        stage('Push to Docker Hub') {
            steps {
                sh "echo \$DOCKER_HUB_CRED_PSW | docker login -u \$DOCKER_HUB_CRED_USR --password-stdin"
                sh "docker push ${IMAGE_NAME}:${BUILD_NUMBER}"
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }
    }

    post {
        always {
            sh "docker logout"
            cleanWs() // Keeps your Jenkins VM clean
        }
    }
}
