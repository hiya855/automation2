pipeline {
    agent any

    environment {
        // ID must match the Credential ID you create in Jenkins
        DOCKER_HUB_CRED = credentials('docker-hub-id')
        IMAGE_NAME = "hiya855/automation"
        DOCKER_API_VERSION = "1.44"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest ."
            }
        }

       # stage('Security Scan (Trivy)') {
       #     steps {
       #         sh "trivy image --severity HIGH,CRITICAL --docker-host unix:///var/run/docker.sock ${IMAGE_NAME}:latest"
       #     }
       # }

        stage('Push to Docker Hub') {
            steps {
                sh "echo \$DOCKER_HUB_CRED_PSW | docker login -u \$DOCKER_HUB_CRED_USR --password-stdin"
                sh "docker push ${IMAE_NAME}:${BUILD_NUMBER}"
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }
    } // Added missing brace to close 'stages'

    post {
        always {
            // Logout and cleanup
            sh "docker logout"
            cleanWs() 

            // Sending email notification via SMTP
            echo "-------- DEBUG: POST BLOCK IS RUNNING --------"
            mail to: 'karanpuriahiya@gmail.com',
                 subject: "Jenkins Build ${currentBuild.fullDisplayName}: ${currentBuild.result ?: 'SUCCESS'}",
                 body: "Build Process Finished.\n\nProject: ${env.JOB_NAME}\nBuild Number: ${env.BUILD_NUMBER}\nConsole Output: ${env.BUILD_URL}console"
        }
    }
}
