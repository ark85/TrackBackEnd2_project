up:
	docker-compose up
test: up
	docker-compose exec stack_app python3 /app/manage.py test
migrate: up
	docker-compose exec stack_app python3 /app/manage.py migrate
run: up
	docker-compose exec stack_app python3 /app/manage.py runserver
