# PostgreSQL 11 cluster
init:
	docker-compose -f docker/docker-compose.yaml up -d

reinit:
	docker-compose -f docker/docker-compose.yaml down
	docker-compose -f docker/docker-compose.yaml up -d

stop:
	docker-compose -f docker/docker-compose.yaml down

status:
	docker ps  --filter "ancestor=cassandra"