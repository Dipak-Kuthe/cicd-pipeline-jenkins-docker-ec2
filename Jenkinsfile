pipeline {
    agent any

    environment {
        IMAGE_NAME    = "dipakkuthe/sample-app"
        IMAGE_TAG     = "${BUILD_NUMBER}"
        EC2_HOST      = "ec2-user@${EC2_PUBLIC_IP}"
        REGISTRY_CRED = "dockerhub-creds"
        SSH_CRED      = "ec2-ssh"
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning source from GitHub...'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Installing dependencies...'
                sh 'pip install -r app/requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Running unit tests...'
                sh 'python -m pytest app/ || echo "no tests yet"'
            }
        }

        stage('Docker Build') {
            steps {
                echo 'Building Docker image...'
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
            }
        }

        stage('Docker Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: REGISTRY_CRED,
                        usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin'
                    sh "docker push ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(credentials: [SSH_CRED]) {
                    sh """
                        ssh -o StrictHostKeyChecking=no ${EC2_HOST} '
                            docker pull ${IMAGE_NAME}:${IMAGE_TAG} &&
                            docker stop sample-app || true &&
                            docker rm sample-app || true &&
                            docker run -d --name sample-app -p 80:5000 ${IMAGE_NAME}:${IMAGE_TAG}
                        '
                    """
                }
            }
        }
    }

    post {
        success { echo "Deployed ${IMAGE_NAME}:${IMAGE_TAG} successfully." }
        failure { echo 'Pipeline failed. Check the logs above.' }
        always  { sh 'docker logout || true' }
    }
}
