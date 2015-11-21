ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
MANAGE=./manage.py
APP=antisocial
FLAKE8=./ve/bin/flake8

ifeq ($(TAG), undefined)
	IMAGE = thraxil/$(APP)
else
	IMAGE = thraxil/$(APP):$(TAG)
endif


jenkins: ./ve/bin/python validate test flake8

./ve/bin/python: requirements.txt bootstrap.py virtualenv.py
	./bootstrap.py

test: ./ve/bin/python
	$(MANAGE) jenkins

flake8: ./ve/bin/python
	$(FLAKE8) $(APP) --max-complexity=10

runserver: ./ve/bin/python validate
	$(MANAGE) runserver

migrate: ./ve/bin/python validate
	$(MANAGE) migrate

validate: ./ve/bin/python
	$(MANAGE) validate

shell: ./ve/bin/python
	$(MANAGE) shell_plus

clean:
	rm -rf ve
	rm -rf media/CACHE
	rm -rf reports
	rm celerybeat-schedule
	rm .coverage
	find . -name '*.pyc' -exec rm {} \;

pull:
	git pull
	make validate
	make test
	make migrate
	make flake8

rebase:
	git pull --rebase
	make validate
	make test
	make migrate
	make flake8

collectstatic: ./ve/bin/python validate
	$(MANAGE) collectstatic --noinput --settings=$(APP).settings_production

compress: ./ve/bin/python validate
	$(MANAGE) compress --settings=$(APP).settings_production

deploy: ./ve/bin/python validate jenkins
	git push
	./ve/bin/fab deploy

travis_deploy: ./ve/bin/python validate jenkins
	./ve/bin/fab deploy -i antisocial_rsa

# run this one the very first time you check
# this out on a new machine to set up dev
# database, etc. You probably *DON'T* want
# to run it after that, though.
install: ./ve/bin/python validate jenkins
	createdb $(APP)
	$(MANAGE) syncdb --noinput
	make migrate

wheelhouse/requirements.txt: requirements.txt
	mkdir -p wheelhouse
	docker run --rm \
	-v $(ROOT_DIR):/app \
	-v $(ROOT_DIR)/wheelhouse:/wheelhouse \
	ccnmtl/django.build
	cp requirements.txt wheelhouse/requirements.txt
	touch wheelhouse/requirements.txt

build: wheelhouse/requirements.txt
	docker build -t $(IMAGE) .
