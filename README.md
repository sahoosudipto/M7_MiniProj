    brew install awscli
    aws configure

# Build the Docker image
docker build -t patient-survival-prediction-app -f Dockerfile .


###git repo
Create a New GitHub Repository
Do not initialize with a README, .gitignore, or license

cd /path/to/M7_MINIPROJ 
git init                 
git add .   # Stage all files add only required files
#use git reset to remove unwanted files
#git reset venv/
git commit -m "Initial commit"   # Commit all files
#remote origin
git remote add origin https://github.com/sahoosudipto/M7_MiniProj.git

#push the chages
#git push -u origin master
#if branch is ma
git push -u origin main

###### step 3 run code in codespace
createa new codespace
pip install -r PatientSurvivalPrediction/requirements.txt

#docker build .
docker build -t patient-survival-prediction-app:v1.0 .

docker image ls

##aws configuration
pip install awscli
Add two secrets:
    AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY
aws configure

#check the docker image size
docker images | grep patient-survival-prediction-app | awk '{print $5}'


###### step 4 Run docker container and access the application
docker build -t patient-survival-prediction-app .
docker run -it -p 5000:5000 patient-survival-prediction-app

docker login -u aimlc3sudipto
dckr_pat_yA8JMoi0K-fYIFIrM8eDksYn3TA

#add tag
docker tag patient-survival-prediction-app aimlc3sudipto/patient-survival-prediction-app:latest
#docker push
docker push aimlc3sudipto/patient-survival-prediction-app:latest

###### step 5 Push docker image to ECR

1. Create an ECR Repository - patient-survival-prediction-app
url: 209479294157.dkr.ecr.eu-north-1.amazonaws.com/patient-survival-prediction-app
#push

export AWS_TTY=1
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 209479294157.dkr.ecr.eu-north-1.amazonaws.com


aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 209479294157.dkr.ecr.eu-north-1.amazonaws.com
docker tag patient-survival-prediction-app:latest 209479294157.dkr.ecr.eu-north-1.amazonaws.com/patient-survival-prediction-app:latest
docker push 209479294157.dkr.ecr.eu-north-1.amazonaws.com/patient-survival-prediction-app:latest


##### step 6 Deploy application with ECS
1.  Create an ECS Cluster:
2. Create a Task Definition
    Container Definitions - 209479294157.dkr.ecr.eu-north-1.amazonaws.com/patient-survival-prediction-app:latest
3. Create a Service
    service name - patient-survival-prediction-app-service    
4. Accessing the Application

#### step 7 cleanup
1. Delete the ECS Service
2. Delete the Task Definition
3. Delete the Cluster
4. Delete the ECR Repository
