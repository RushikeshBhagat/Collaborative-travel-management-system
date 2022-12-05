pipeline {
    environment {
        
        def imageName = "avadhut007/cloudcomputings:v1-${env.BRANCH_NAME}-${env.BUILD_ID}"
        DOCKERHUB_CREDENTIALS=credentials('1c1edff8-6e15-45ef-b29e-b6f691662587')

    }

    agent any 
        stages {

            stage("Build the Docker Image") {
                steps{
                    script {
                        sh "docker build -t ${imageName} ."
                    }
                }
            }
        
            stage("Push Image to the Docker Registry") {
                steps{
                    script {
                        sh 'echo $DOCKERHUB_CREDENTIALS_PSW | docker login -u $DOCKERHUB_CREDENTIALS_USR --password-stdin'
                        sh "docker push ${imageName}"
                    }
                }
            }
             stage ('Remove Previous App Container') {
                steps {
                    echo 'Hello, '

                    sh '''#!/bin/bash
                        echo "START"
                        for id in $(docker ps -q)
                            do
                                echo "stopping container ${id}"
                                docker stop "${id}"
                                echo "DONE"
                            done
                    '''
                }
            }                  
            stage("Deploy New App Container on VM") {
                when{
                        branch 'master'
                    }
                steps{
                    script {
                        sh "docker pull ${imageName}"
                        sh "docker run -dt -p 5000:5000 ${imageName}"
                    }
                }
            }
            
        }

}
