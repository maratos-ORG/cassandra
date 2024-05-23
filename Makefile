init:
	docker-compose -f docker-compose.yaml up -d

reinit:
	docker-compose -f docker-compose.yaml down
	docker-compose -f docker-compose.yaml up -d

stop:
	docker-compose -f docker-compose.yaml down

status:
	docker ps  --filter "ancestor=cassandra"

clean: stop
	rm -rf docker/data/cassandra1/*
	rm -rf docker/data/cassandra2/*
	rm -rf docker/data/cassandra3/*