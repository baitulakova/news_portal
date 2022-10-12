make:
	docker-compose down --remove-orphans
	docker-compose up --build
	
test:
	docker-compose -f docker-compose_test.yml up --build -d
	docker-compose -f docker-compose_test.yml down
