cd /home/app/nexcruise
sudo docker-compose -f docker-compose-dev.yml down
sudo docker-compose -f docker-compose-stage.yml down
git checkout staging
git pull origin staging
sudo docker-compose -f docker-compose-stage.yml up --build -d
