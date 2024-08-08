run:
	docker compose -f docker-compose.yaml up --force-recreate --remove-orphans

crun:
	docker compose -f docker-compose.yaml up --force-recreate --remove-orphans --build

format:
	black .

test:
	docker exec selenium-tech-task-web-1 pytest > test_result

# venv:
# 	source .venv/bin/activate
