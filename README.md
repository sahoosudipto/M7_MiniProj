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
git push -u origin master
