bash:
	@docker-compose exec backend bash

shell:
	@docker-compose exec backend bash -c "python manage.py shell_plus"

#backup:
#	@docker-compose exec postgres bash -c "export PGPASSWORD=$(POSTGRES_PASSWORD) && pg_dump -d $(POSTGRES_DB) -U $(POSTGRES_USER) > /tmp/$(FILE_NAME)" && docker cp peak-delivery_postgres_1:/tmp/$(FILE_NAME) .

dbshell:
	@docker-compose exec backend bash -c "python manage.py dbshell"

makemigrations:
	@docker-compose exec backend bash -c "python manage.py makemigrations"

makedatamigrations:
	@docker-compose exec backend bash -c "python manage.py makemigrations --empty $(app)"

squashmigrations:
	@docker-compose exec backend bash -c "python manage.py squashmigrations"

migrate:
	@docker-compose exec backend bash -c "python manage.py migrate"

reqs:
	@docker-compose exec backend bash -c "pip install -r requirements.txt"

load_blocks:
	@docker-compose exec backend bash -c "python manage.py loaddata blocks"

dump_blocks:
	@docker-compose exec backend bash -c "python manage.py dumpdata promotions --indent=4 > blocks.json"

install_docker:
	@sh get-docker.sh
	@sudo apt-get install -y docker-compose

update_code:
	@git pull
	@docker-compose stop
	@docker-compose up -d

resetdb:
	@echo "Creating an empty database"
	@docker-compose rm -sf postgres
	@docker-compose up -d postgres

dev_setup:
	@./shell_inside_docker.sh "./manage.py makemigrations"
	@./shell_inside_docker.sh "./manage.py migrate"
	@./shell_inside_docker.sh "./dev_setup.sh"

create_superuser:
	@docker-compose exec backend bash -c "python manage.py createsuperuser"

test:
	@docker-compose exec backend bash -c "python manage.py test"
