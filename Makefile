ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
MANAGE=./manage.py
APP=antisocial
REPO=thraxil
FLAKE8=./ve/bin/flake8
PYTHON=./ve/bin/python
MAX_COMPLEXITY=5
WHEELHOUSE=wheelhouse

ifeq ($(TAG), undefined)
	IMAGE = $(REPO)/$(APP)
else
	IMAGE = $(REPO)/$(APP):$(TAG)
endif

jenkins: $(PYTHON) validate test flake8

$(PYTHON): requirements.txt bootstrap.py virtualenv.py
	./bootstrap.py

test: $(PYTHON)
	$(MANAGE) jenkins

flake8: $(PYTHON)
	$(FLAKE8) $(APP) --max-complexity=$(MAX_COMPLEXITY)

runserver: $(PYTHON) validate
	$(MANAGE) runserver

migrate: $(PYTHON) validate
	$(MANAGE) migrate

validate: $(PYTHON)
	$(MANAGE) validate

shell: $(PYTHON)
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

collectstatic: $(PYTHON) validate
	$(MANAGE) collectstatic --noinput --settings=$(APP).settings_production

compress: $(PYTHON) validate
	$(MANAGE) compress --settings=$(APP).settings_production

# run this one the very first time you check
# this out on a new machine to set up dev
# database, etc. You probably *DON'T* want
# to run it after that, though.
install: $(PYTHON) validate jenkins
	createdb $(APP)
	$(MANAGE) syncdb --noinput
	make migrate

$(WHEELHOUSE)/requirements.txt: requirements.txt
	mkdir -p $(WHEELHOUSE)
	docker run --rm \
	-v $(ROOT_DIR):/app \
	-v $(ROOT_DIR)/$(WHEELHOUSE):/wheelhouse \
	ccnmtl/django.build
	cp requirements.txt $(WHEELHOUSE)/requirements.txt
	touch $(WHEELHOUSE)/requirements.txt

build: $(WHEELHOUSE)/requirements.txt
	docker build -t $(IMAGE) .

.PHONY: clean collectstatic compress build install pull rebase shell validate migrate runserver flake8 test jenkins
