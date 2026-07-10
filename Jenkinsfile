pipeline {
    agent any

    environment {
                MONGO_URI = credentials('abhash-mongo-uri')
                SECRET_KEY = credentials('abhash-mongo-secret-key')
            }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh '''
                    echo "===== Build Stage ====="
                    echo "Creating .env file..."

                cat > .env <<EOF
MONGO_URI=$MONGO_URI
SECRET_KEY=$SECRET_KEY
EOF

                    python3 --version

                    echo "Contents of workspace:"
                    ls -la

                    python3 -m pip install --upgrade pip --break-system-packages

                    python3 -m pip install -r requirements.txt --break-system-packages
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    echo "===== Test Stage ====="

                    python3 -m pytest -v
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    echo "===== Deploy Stage ====="

                    # Remove old deployment folder if it exists
                    rm -rf deployment

                    # Create deployment directory
                    mkdir deployment

                    # Copy only required application files
                    cp app.py deployment/
                    cp requirements.txt deployment/
                    cp README.md deployment/
                    cp -r templates deployment/

                    echo "Deployment completed successfully."

                    echo "===== Deployment Files ====="
                    ls -R deployment
                '''
            }
        }
    }

     post {

        success {
            emailext(
                to: 'imabhash@gmail.com',
                subject: "✅ SUCCESS: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
    Hello,
    
    The Jenkins pipeline completed successfully.
    
    Job Name     : ${env.JOB_NAME}
    Build Number : ${env.BUILD_NUMBER}
    Status       : SUCCESS
    
    The Flask application was:
    ✔ Checked out
    ✔ Built
    ✔ Tested
    ✔ Deployed successfully
    ✔ Verified Deployment
    
    Build URL:
    ${env.BUILD_URL}
    
    Regards,
    Jenkins CI/CD
    """
            )
        }
    
        failure {
            emailext(
                to: 'imabhash@gmail.com',
                subject: "❌ FAILED: ${env.JOB_NAME} #${env.BUILD_NUMBER}",
                body: """
    Hello,
    
    The Jenkins pipeline has failed.
    
    Job Name     : ${env.JOB_NAME}
    Build Number : ${env.BUILD_NUMBER}
    Status       : FAILURE
    
    Please review the console output for error details.
    
    Build URL:
    ${env.BUILD_URL}
    
    Regards,
    Jenkins CI/CD
    """
            )
        }
    }
}
