pipeline {
    agent any

    environment {
        IMAGE_NAME = "flask_todo_app"
        CONTAINER_NAME = "flask_todo_container"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'dev', url: 'https://github.com/JakaxKato/repo.git' // ganti sesuai repo kamu
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build(IMAGE_NAME)
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    docker.image(IMAGE_NAME).inside {
                        sh 'pip install pytest'
                        sh 'pytest tests/'  // Asumsikan test ada di folder tests/
                    }
                }
            }
        }

        stage('Security Scan') {
            steps {
                script {
                    docker.image(IMAGE_NAME).inside {
                        sh 'pip install bandit'
                        sh 'bandit -r .'
                    }
                }
            }
        }

        stage('Deploy to VM') {
            steps {
                script {
                    // Stop dan hapus container lama jika ada
                    sh "docker rm -f ${CONTAINER_NAME} || true"

                    // Jalankan container baru
                    sh "docker run -d --name ${CONTAINER_NAME} -p 5000:5000 ${IMAGE_NAME}"
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline selesai dengan sukses!'
        }
        failure {
            echo 'Pipeline gagal, cek log untuk detilnya.'
        }
    }
}
