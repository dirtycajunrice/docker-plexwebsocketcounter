pipeline {
    agent none
    environment {
        REPOSITORY = "dirtycajunrice/plexwebsocketcounter"
        VERSION_FILE = "ws_counter.py"
        FLAKE_FILES = "ws_counter.py"
        TAG = ""
    }
    stages {
        stage('Flake8') {
            agent { label 'amd64'}
            steps {
                sh '''
                    python3 -m venv venv && venv/bin/pip install flake8 && venv/bin/python -m flake8 --max-line-length 120 ${FLAKE_FILES}
                    rm -rf venv/
                '''
                script {
                    TAG = sh(returnStdout: true, script: 'grep -i version ${VERSION_FILE} | cut -d" " -f3 | tr -d \\"').trim()
                }
            }
        }
        stage('Docker Builds') {
            parallel {
                stage('amd64') {
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
                                def image = docker.build("${REPOSITORY}:${TAG}-amd64")
                                image.push()
                                
                            } else if (BRANCH_NAME == 'develop') {
                                def image = docker.build("${REPOSITORY}:develop-amd64")
                                image.push()
                            }
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
                                def image = docker.build("${REPOSITORY}:${TAG}-arm", "-f Dockerfile.arm .")
                                image.push()
                            } else if (BRANCH_NAME == 'develop') {
                                def image = docker.build("${REPOSITORY}:develop-arm", "-f Dockerfile.arm .")
                                image.push()
                            }
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
                                def image = docker.build("${REPOSITORY}:${TAG}-arm64", "-f Dockerfile.arm64 .")
                                image.push()
                            } else if (BRANCH_NAME == 'develop') {
                                def image = docker.build("${REPOSITORY}:develop-arm64", "-f Dockerfile.arm64 .")
                                image.push()
                            }
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
                        sh(script: "docker manifest create ${REPOSITORY}:${TAG} ${REPOSITORY}:${TAG}-amd64 ${REPOSITORY}:${TAG}-arm64 ${REPOSITORY}:${TAG}-arm")
                        sh(script: "docker manifest inspect ${REPOSITORY}:${TAG}")
                        sh(script: "docker manifest push -p ${REPOSITORY}:${TAG}")
                        sh(script: "docker manifest create ${REPOSITORY}:latest ${REPOSITORY}:${TAG}-amd64 ${REPOSITORY}:${TAG}-arm64 ${REPOSITORY}:${TAG}-arm")
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
        stage('GitHub Release') {
            when { branch 'master' }
            agent { label 'amd64'}
            steps {
                sh '''
                    git tag ${TAG} && git push --tags
                '''
            }
        }
    }
}
