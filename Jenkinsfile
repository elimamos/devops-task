
pipeline {
    agent {
          label 'slave1'
     }//agent
      environment {
        DATA_SOURCE="https://www.ibike.org/library/statistics-data.htm"
     }
    stages {
       stage("Get page source") {
          steps {
              sh "chmod +x getData.py"
              sh "python3 ./getData.py -u ${DATA_SOURCE}"
          }//steps
       }//stage
       stage("Archive artifacts"){
           steps{
               archiveArtifacts artifacts: '*.png, *.csv'
           }
       }
    }//stages
}//pipeline
