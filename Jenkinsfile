def imageName="192.168.44.44:8082/docker-local/frontend"
def dockerRegistry="https://192.168.44.44:8082"
def registryCredentials="artifactory"
def dockerTag=""

pipeline {
    agent {
        label 'agent'
    }

    stages {
        stage('Get code') {
            steps {
                // CGet code from github repo
                checkout scm
            }
        }
        stage('Show files') {
            steps {
                // print files
                sh 'ls -la'
            }
        }
        stage('Run unit tests') {
            steps {
                // install requirements
                sh 'pip3 install -r requirements.txt'
                sh 'python3 -m pytest --cov=. --cov-report xml:test-results/coverage.xml --junitxml=test-results/pytest-report.xml'
            }
        }
        stage('sonarqube') {
            environment {
              scannerHome = tool 'SonarQube'
            }
            steps {
                withSonarQubeEnv('SonarQube') { 
                sh "${scannerHome}/bin/sonar-scanner"
                }
                timeout(1){
                    // Parameter indicates whether to set pipeline to UNSTABLE if Quality Gate fails
                    // true = set pipeline to UNSTABLE, false = don't
                    waitForQualityGate abortPipeline: true
                }
            }    
        }
        stage('Build app image'){
            steps{
                script{
                    dockerTag = "RC-${env.BUILD_ID}.${env.GIT_COMMIT.take(7)}"
                    applicationImage = docker.build("$imageName:$dockerTag",".")
                }
            }
        }
        stage('Push image'){
            steps{
                script{
                    docker.withRegistry("$dockerRegistry", "$registryCredentials") {
                        applicationImage.push()
                        applicationImage.push('latest')
                    }
                }
            }
        }
    }
    post {
        always {
            junit "test-results/*.xml"
            cleanWs()
        }
    }
}