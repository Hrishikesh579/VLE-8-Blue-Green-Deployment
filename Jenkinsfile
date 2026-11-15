pipeline {
    agent any

    triggers {
        pollSCM('H/2 * * * *')
    }

    environment {
        EC2_HOST = '18.61.25.99'

        APP_NAME = 'vle8-blue-green-app'

        K8S_NAMESPACE = 'vle8'

        BLUE_DEPLOYMENT = 'vle8-app-blue'
        GREEN_DEPLOYMENT = 'vle8-app-green'

        SERVICE_NAME = 'vle8-app-service'
        CONTAINER_NAME = 'app'
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Validate Project') {
            steps {
                bat '''
                    @echo off

                    if not exist app\\Dockerfile exit /b 1
                    if not exist app\\server.py exit /b 1
                    if not exist app\\index.html exit /b 1

                    if not exist kubernetes\\namespace.yaml exit /b 1
                    if not exist kubernetes\\deployment-blue.yaml exit /b 1
                    if not exist kubernetes\\deployment-green.yaml exit /b 1
                    if not exist kubernetes\\service.yaml exit /b 1

                    echo Project validation successful.
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'vle8-dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    bat '''
                        @echo off

                        docker build ^
                          -t %DOCKERHUB_USER%/%APP_NAME%:%BUILD_NUMBER% ^
                          ./app

                        if errorlevel 1 exit /b 1
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'vle8-dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    bat '''
                        @echo off

                        echo %DOCKERHUB_TOKEN%| docker login ^
                          -u %DOCKERHUB_USER% ^
                          --password-stdin

                        if errorlevel 1 exit /b 1

                        docker push %DOCKERHUB_USER%/%APP_NAME%:%BUILD_NUMBER%

                        if errorlevel 1 exit /b 1

                        docker logout
                    '''
                }
            }
        }

        stage('Deploy Green') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'vle8-dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    ),
                    sshUserPrivateKey(
                        credentialsId: 'vle8-ec2-ssh-key',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                    bat '''
                        @echo off

                        ssh -i "%SSH_KEY%" ^
                          -o StrictHostKeyChecking=accept-new ^
                          %SSH_USER%@%EC2_HOST% ^
                          "sudo kubectl -n %K8S_NAMESPACE% set image deployment/%GREEN_DEPLOYMENT% %CONTAINER_NAME%=%DOCKERHUB_USER%/%APP_NAME%:%BUILD_NUMBER% && sudo kubectl -n %K8S_NAMESPACE% rollout status deployment/%GREEN_DEPLOYMENT% --timeout=180s"

                        if errorlevel 1 exit /b 1
                    '''
                }
            }
        }

        stage('Verify Green') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'vle8-ec2-ssh-key',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                    bat '''
                        @echo off

                        ssh -i "%SSH_KEY%" ^
                          -o StrictHostKeyChecking=accept-new ^
                          %SSH_USER%@%EC2_HOST% ^
                          "sudo kubectl get deployment %GREEN_DEPLOYMENT% -n %K8S_NAMESPACE% && sudo kubectl get pods -n %K8S_NAMESPACE% -l app=vle8-app,color=green"

                        if errorlevel 1 exit /b 1
                    '''
                }
            }
        }

        stage('Approve Traffic Switch') {
            steps {
                timeout(time: 15, unit: 'MINUTES') {
                    input(
                        message: 'Green deployment is ready. Switch live traffic from Blue to Green?',
                        ok: 'Switch Traffic to Green'
                    )
                }
            }
        }

        stage('Switch Traffic to Green') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'vle8-ec2-ssh-key',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                    bat '''
                        @echo off

                        ssh -i "%SSH_KEY%" ^
                          -o StrictHostKeyChecking=accept-new ^
                          %SSH_USER%@%EC2_HOST% ^
                          "sudo kubectl set selector service/%SERVICE_NAME% -n %K8S_NAMESPACE% app=vle8-app,color=green"

                        if errorlevel 1 exit /b 1
                    '''
                }
            }
        }

        stage('Verify Traffic Switch') {
            steps {
                withCredentials([
                    sshUserPrivateKey(
                        credentialsId: 'vle8-ec2-ssh-key',
                        keyFileVariable: 'SSH_KEY',
                        usernameVariable: 'SSH_USER'
                    )
                ]) {
                    bat '''
                        @echo off

                        ssh -i "%SSH_KEY%" ^
                          -o StrictHostKeyChecking=accept-new ^
                          %SSH_USER%@%EC2_HOST% ^
                          "sudo kubectl get service %SERVICE_NAME% -n %K8S_NAMESPACE% -o yaml && sudo kubectl get endpoints %SERVICE_NAME% -n %K8S_NAMESPACE%"

                        if errorlevel 1 exit /b 1
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'VLE-8 Blue-Green deployment completed successfully.'
        }

        failure {
            echo 'Pipeline failed. Inspect the failed stage before proceeding.'
        }

        always {
            echo 'VLE-8 pipeline execution finished.'
        }
    }
}