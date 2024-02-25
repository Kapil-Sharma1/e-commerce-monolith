cd /home/app/nexcruise-v2/nexcruise
sudo docker-compose -f docker-compose-dev.yml down
git checkout develop
git pull origin develop
# sudo docker-compose -f docker-compose-dev.yml build nodereact
sudo docker-compose -f docker-compose-dev.yml up --build -d backend
