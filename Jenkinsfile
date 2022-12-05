pipeline {
    environment {
        
        def imageName = "avadhut007/cloudcomputings:v1-${env.BRANCH_NAME}-${env.BUILD_ID}"

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
                        sh "docker push ${imageName}"
                    }
                }
            }
             stage ('Remove Previous App Container') {
                steps {
                    echo 'Hello, '

                    sh '''#!/bin/bash
                        for id in $(docker ps -q)
                        do
                            if [[ $(docker port "${id}") == 5000 ]]; then
                                echo "stopping container ${id}"
                                docker stop "${id}"
                            fi
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
