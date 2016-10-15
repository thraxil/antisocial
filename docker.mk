ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

build:
	docker build -t $(IMAGE) .

docker-pg:
	docker run --name $(APP)-pg \
	-e POSTGRES_PASSWORD=nothing \
	-e POSTGRES_USER=postgres \
	-d \
	postgres

docker-test: build
	docker run -it -p 31000:8000 \
	--link $(APP)-pg:postgresql \
	-e DB_NAME=postgres \
	-e SECRET_KEY=notreal \
	-e DB_PASSWORD=nothing \
	-e DB_USER=postgres \
	$(REPO)/$(APP)

.PHONY: build docker-pg docker-test
