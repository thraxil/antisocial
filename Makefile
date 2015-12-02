ROOT_DIR:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VE=./ve
MANAGE=./manage.py
APP=antisocial
REPO=thraxil
FLAKE8=$(VE)/bin/flake8
PYTHON=$(VE)/bin/python
SYS_PYTHON=python
PIP=$(VE)/bin/pip
SENTINAL=$(VE)/sentinal
MAX_COMPLEXITY=5
WHEELHOUSE=wheelhouse
PYPI_URL=https://pypi.ccnmtl.columbia.edu/
WHEEL_VERSION=0.24.0
REQUIREMENTS=requirements.txt
VIRTUALENV=virtualenv.py
SUPPORT_DIR=requirements/virtualenv_support/

ifeq ($(TAG), undefined)
	IMAGE = $(REPO)/$(APP)
else
	IMAGE = $(REPO)/$(APP):$(TAG)
endif

jenkins: $(SENTINAL) validate test flake8

$(SENTINAL): $(REQUIREMENTS) $(VIRTUALENV) $(SUPPORT_DIR)*
	rm -rf $(VE)
	$(SYS_PYTHON) $(VIRTUALENV) --extra-search-dir=$(SUPPORT_DIR) --never-download $(VE)
	$(PIP) install --index-url=$(PYPI_URL) wheel==$(WHEEL_VERSION)
	$(PIP) install --use-wheel --no-deps --index-url=$(PYPI_URL) --requirement $(REQUIREMENTS)
	$(SYS_PYTHON) $(VIRTUALENV) --relocatable $(VE)
	touch $(SENTINAL)

test: $(SENTINAL)
	$(MANAGE) jenkins

flake8: $(SENTINAL)
	$(FLAKE8) $(APP) --max-complexity=$(MAX_COMPLEXITY)

runserver: $(SENTINAL) validate
	$(MANAGE) runserver

migrate: $(SENTINAL) validate
	$(MANAGE) migrate

validate: $(SENTINAL)
	$(MANAGE) validate

shell: $(SENTINAL)
	$(MANAGE) shell_plus

clean:
	rm -rf $(VE)
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

collectstatic: $(SENTINAL) validate
	$(MANAGE) collectstatic --noinput --settings=$(APP).settings_production

compress: $(SENTINAL) validate
	$(MANAGE) compress --settings=$(APP).settings_production

# run this one the very first time you check
# this out on a new machine to set up dev
# database, etc. You probably *DON'T* want
# to run it after that, though.
install: $(SENTINAL) validate jenkins
	createdb $(APP)
	$(MANAGE) syncdb --noinput
	make migrate

$(WHEELHOUSE)/requirements.txt: $(REQUIREMENTS)
	mkdir -p $(WHEELHOUSE)
	docker run --rm \
	-v $(ROOT_DIR):/app \
	-v $(ROOT_DIR)/$(WHEELHOUSE):/wheelhouse \
	ccnmtl/django.build
	cp $(REQUIREMENTS) $(WHEELHOUSE)/requirements.txt
	touch $(WHEELHOUSE)/requirements.txt

build: $(WHEELHOUSE)/requirements.txt
	docker build -t $(IMAGE) .

.PHONY: clean collectstatic compress build install pull rebase shell validate migrate runserver flake8 test jenkins
