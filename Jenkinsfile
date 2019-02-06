pipeline {
    agent none
    environment {
        REPOSITORY = "dirtycajunrice/plexwebsocketcounter"
    }
    stages {
        stage('Docker x86 Build') {
            when {
                anyOf {
                    branch 'master'
                    branch 'develop'
                }
            }
            agent { node 'x86Node1'}
            steps {
                script {
                    if (BRANCH_NAME == 'master') {
                        def tag = sh(returnStdout: true, script: 'grep -i version ws_counter.py | cut -d" " -f3 | tr -d \\"').trim()
                        def image = docker.build("${REPOSITORY}:${tag}-amd64")
                        image.push()
                        image.push("latest-amd64")
                    } else if (BRANCH_NAME == 'develop') {
                        def image = docker.build("${REPOSITORY}:develop-amd64")
                        image.push()
                    }
                }
            }
        }
        stage('Docker ARM Builds') {
            when {
                anyOf {
                    branch 'master'
                    branch 'develop'
                }
            }
            agent { node 'CajunARM64'}
            steps {
                script {
                    if (BRANCH_NAME == 'master') {
                        def tag = sh(returnStdout: true, script: 'grep -i version ws_counter.py | cut -d" " -f3 | tr -d \\"').trim()
                        def armimage = docker.build("${REPOSITORY}:${tag}-arm", "-f Dockerfile.arm .")
                        def arm64image = docker.build("${REPOSITORY}:${tag}-arm64", "-f Dockerfile.arm64 .")
                        armimage.push()
                        arm64image.push()
                        armimage.push("latest-arm")
                        arm64image.push("latest-arm64")
                    } else if (BRANCH_NAME == 'develop') {
                        def armimage = docker.build("${REPOSITORY}:develop-arm", "-f Dockerfile.arm .")
                        def arm64image = docker.build("${REPOSITORY}:develop-arm64", "-f Dockerfile.arm64 .")
                        armimage.push()
                        arm64image.push()
                    }
                }
            }
        }
        stage('Docker Manifest Build') {
            when {
                anyOf {
                    branch 'master'
                    branch 'develop'
                }
            }
            agent { node 'x86Node1'}
            steps {
                script {
                    if (BRANCH_NAME == 'master') {
                        def tag = sh(returnStdout: true, script: 'grep -i version ws_counter.py | cut -d" " -f3 | tr -d \\"').trim()
                        sh(script: "docker manifest create ${REPOSITORY}:${tag} ${REPOSITORY}:${tag}-amd64 ${REPOSITORY}:${tag}-arm64 ${REPOSITORY}:${tag}-arm")
                        sh(script: "docker manifest inspect ${REPOSITORY}:${tag}")
                        sh(script: "docker manifest push -p ${REPOSITORY}:${tag}")
                        sh(script: "docker manifest create ${REPOSITORY}:latest ${REPOSITORY}:latest-amd64 ${REPOSITORY}:latest-arm64 ${REPOSITORY}:latest-arm")
                        sh(script: "docker manifest inspect ${REPOSITORY}:latest")
                        sh(script: "docker manifest push -p ${REPOSITORY}:latest")
                    } else if (BRANCH_NAME == 'develop') {
                        sh(script: "docker manifest create ${REPOSITORY}:develop ${REPOSITORY}:develop-amd64 ${REPOSITORY}:develop-arm64 ${REPOSITORY}:develop-arm")
                        sh(script: "docker manifest inspect ${REPOSITORY}:develop")
                        sh(script: "docker manifest push -p ${REPOSITORY}:develop")
                    }
                }
            }
        }
    }
}
