make:
	docker-compose down --remove-orphans
	docker-compose up --build
	
test:
	docker-compose -f docker-compose_test.yml up --build --abort-on-container-exit
	docker-compose -f docker-compose_test.yml down
