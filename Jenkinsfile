pipeline {
    agent none
    environment {
        REPOSITORY = "dirtycajunrice/plexwebsocketcounter"
    }
    stages {
        stage('Flake8') {
            agent { label 'amd64'}
            steps {
                sh '''
                    python3 -m venv ouro-venv && ouro-venv/bin/pip install flake8 && ouro-venv/bin/python -m flake8 --max-line-length 120 *.py
                    rm -rf ouro-venv/
                '''
            }
        }
        stage('Docker Builds') {
            parallel {
                stage('x86') {
                    when {
                        anyOf {
                            branch 'master'
                            branch 'develop'
                        }
                    }
                    agent { label 'amd64'}
                    steps {
                        script {
                            if (BRANCH_NAME == 'master') {
                                def tag = sh(returnStdout: true, script: 'grep -i version ws_counter.py | cut -d" " -f3 | tr -d \\"').trim()
                                def image = docker.build("${REPOSITORY}:${tag}-amd64")
                                
                            } else if (BRANCH_NAME == 'develop') {
                                def image = docker.build("${REPOSITORY}:develop-amd64")
                            }
                            image.push()
                        }
                    }
                }
                stage('ARMv6') {
                    when {
                        anyOf {
                            branch 'master'
                            branch 'develop'
                        }
                    }
                    agent { label 'arm64'}
                    steps {
                        script {
                            if (BRANCH_NAME == 'master') {
                                def tag = sh(returnStdout: true, script: 'grep -i version ws_counter.py | cut -d" " -f3 | tr -d \\"').trim()
                                def image = docker.build("${REPOSITORY}:${tag}-arm", "-f Dockerfile.arm .")
                            } else if (BRANCH_NAME == 'develop') {
                                def image = docker.build("${REPOSITORY}:develop-arm", "-f Dockerfile.arm .")
                            }
                            image.push()
                        }
                    }
                }
                stage('ARM64v8') {
                    when {
                        anyOf {
                            branch 'master'
                            branch 'develop'
                        }
                    }
                    agent { label 'arm64'}
                    steps {
                        script {
                            if (BRANCH_NAME == 'master') {
                                def tag = sh(returnStdout: true, script: 'grep -i version ws_counter.py | cut -d" " -f3 | tr -d \\"').trim()
                                def image = docker.build("${REPOSITORY}:${tag}-arm64", "-f Dockerfile.arm64 .")
                            } else if (BRANCH_NAME == 'develop') {
                                def image = docker.build("${REPOSITORY}:develop-arm64", "-f Dockerfile.arm64 .")
                            }
                            image.push()
                        }
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
            agent { label 'amd64'}
            steps {
                script {
                    if (BRANCH_NAME == 'master') {
                        def tag = sh(returnStdout: true, script: 'grep -i version ws_counter.py | cut -d" " -f3 | tr -d \\"').trim()
                        sh(script: "docker manifest create ${REPOSITORY}:${tag} ${REPOSITORY}:${tag}-amd64 ${REPOSITORY}:${tag}-arm64 ${REPOSITORY}:${tag}-arm")
                        sh(script: "docker manifest inspect ${REPOSITORY}:${tag}")
                        sh(script: "docker manifest push -p ${REPOSITORY}:${tag}")
                        sh(script: "docker manifest create ${REPOSITORY}:latest ${REPOSITORY}:${tag}-amd64 ${REPOSITORY}:${tag}-arm64 ${REPOSITORY}:${tag}-arm")
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
