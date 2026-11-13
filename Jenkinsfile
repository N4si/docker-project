pipeline {
    agent {label "adnan"}

    stages {
        stage('Code') {
            steps {
                echo 'This is cloning the code'
                git url: "https://github.com/AdnanAttar001/docker-project.git", branch: "main"
            }
        }
        stage('Build') {
            steps {
                echo 'This is building the code'
                sh "docker build -t docker-app ."
            }
        }
        stage('Deploy') {
            steps {
                echo 'This is deploying the code'
                sh "docker run -d -p 5001:5001 docker-app"
            }
        }
    }
}
