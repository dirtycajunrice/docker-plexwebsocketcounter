pipeline {
    agent none
    environment {
        REPOSITORY = "dirtycajunrice/plexwebsocketcounter"
    }
    stages {
        stage('Master x86') {
            when { branch 'master' }
            agent { node 'x86Node1'}
            steps {
                checkout scm
                script {
                    def tag = sh(returnStdout: true, script: 'grep -i version ws_counter.py | cut -d" " -f3 | tr -d \"').trim()
                    def image = docker.build("${REPOSITORY}:${tag}-amd64")
                    image.push()
                    image.push("latest-amd64")
                }
            }
        }
        stage('Master ARM') {
            when { branch 'master' }
            agent { node 'CajunARM64'}
            steps {
                checkout scm
                script {
                    def tag = sh(returnStdout: true, script: 'grep -i version ws_counter.py | cut -d" " -f3 | tr -d \"').trim()
                    def armimage = docker.build("${REPOSITORY}:${tag}-arm", "-f Dockerfile.arm")
                    def arm64image = docker.build("${REPOSITORY}:${tag}-arm64", "-f Dockerfile.arm64")
                    armimage.push()
                    arm64image.push()
                    armimage.push("latest-arm")
                    arm64image.push("latest-arm64")
                }
            }
        }
        stage('Master Manifest') {
            when { branch 'master' }
            agent { node 'x86Node1'}
            steps {
                script {
                    checkout scm
                    def tag = sh(returnStdout: true, script: 'grep -i version ws_counter.py | cut -d" " -f3 | tr -d \"').trim()
                    sh(script: 'docker manifest create "${REPOSITORY}:${tag} ${REPOSITORY}:${tag}-amd64 ${REPOSITORY}:${tag}-arm64 ${REPOSITORY}:${tag}-arm"')
                    sh(script: 'docker manifest create "${REPOSITORY}:latest ${REPOSITORY}:latest-amd64 ${REPOSITORY}:latest-arm64 ${REPOSITORY}:latest-arm"')
                }
            }
        }
        stage('Develop x86') {
            when { branch 'develop' }
            agent { node 'x86Node1'}
            steps {
                checkout scm
                script {
                    def image = docker.build("${REPOSITORY}:develop-amd64")
                    image.push()
                    image.push("develop-amd64")
                }
            }
        }
        stage('Develop ARM') {
            when { branch 'develop' }
            agent { node 'CajunARM64'}
            steps {
                checkout scm
                script {
                    def armimage = docker.build("${REPOSITORY}:develop-arm", "-f Dockerfile.arm")
                    def arm64image = docker.build("${REPOSITORY}:develop-arm64", "-f Dockerfile.arm64")
                    armimage.push()
                    arm64image.push()
                    armimage.push("develop-arm")
                    arm64image.push("develop-arm64")
                }
            }
        }
        stage('Develop Manifest') {
            when { branch 'develop' }
            agent { node 'x86Node1'}
            steps {
                checkout scm
                sh(script: 'docker manifest create "${REPOSITORY}:develop ${REPOSITORY}:develop-amd64 ${REPOSITORY}:develop-arm64 ${REPOSITORY}:develop-arm"')
            }
        }
    }
}
