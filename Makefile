
uml_generarion:
	pyreverse -o jpg src

update_dependencie:
	pip3 freeze > requirements/dev.txt
auto_formater:
	pre-commit run --all-file -c .pre-commit-config.yaml
up:
	docker compose -f docker-compose.yml up -d
base:
	docker compose -f docker-compose-base.yml up --build

build:
	docker compose -f docker-compose.yml down --remove-orphans
	docker compose -f docker-compose.yml up --build

stop:
	docker-compose -f docker-compose.yml down

deploy_aws:
	sh devops/prod-push-to-ecr.sh

logs:
	docker logs ia -f