pipeline {
    agent any

    environment {
        DOCKER_HUB_CRED = credentials('docker-hub-id')
        IMAGE_NAME = "hiya855/automation"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build & Push Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:latest ."
                sh "echo \$DOCKER_HUB_CRED_PSW | docker login -u \$DOCKER_HUB_CRED_USR --password-stdin"
                sh "docker push ${IMAGE_NAME}:latest"
            }
        }

        stage('SSH Deploy via Ansible') {
            steps {
                sh "ansible-playbook -i /automation/inventory.ini /automation/deploy.yml"
            }
        }

        stage('Cleanup Local Images') {
            steps {
                echo "Removing local images to save disk space..."
                // Remove the specific image built in this pipeline
                sh "docker rmi ${IMAGE_NAME}:latest || true"
                // Optional: Remove 'dangling' images (unused layers)
                sh "docker image prune -f"
            }
        }
    }

    post {
        always {
            cleanWs()
            echo "-------- DEBUG: DEPLOYMENT COMPLETE --------"
            mail to: 'karanpuriahiya@gmail.com',
                 subject: "Automation Deployment: ${currentBuild.result ?: 'SUCCESS'}",
                 body: "Build Finished. Access App at: https://unlofty-kitty-glottologic.ngrok-free.dev"
        }
    }
}
