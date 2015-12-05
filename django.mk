jenkins: $(SENTINAL) validate test flake8

test: $(SENTINAL)
	$(MANAGE) test

coverage: $(SENTINAL) flake8
	. $(VE)/bin/activate && $(VE)/bin/coverage run --source='$(APP)' $(MANAGE) test \
	&& $(VE)/bin/coverage html -d reports --omit='*migrations*,*settings_*,*wsgi*'

$(SENTINAL): $(REQUIREMENTS) $(VIRTUALENV) $(SUPPORT_DIR)*
	rm -rf $(VE)
	$(SYS_PYTHON) $(VIRTUALENV) --extra-search-dir=$(SUPPORT_DIR) --never-download $(VE)
	$(PIP) install --index-url=$(PYPI_URL) wheel==$(WHEEL_VERSION)
	$(PIP) install --use-wheel --no-deps --index-url=$(PYPI_URL) --requirement $(REQUIREMENTS)
	$(SYS_PYTHON) $(VIRTUALENV) --relocatable $(VE)
	touch $(SENTINAL)

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

collectstatic: $(SENTINAL) validate
	$(MANAGE) collectstatic --noinput --settings=$(APP).settings_production

compress: $(SENTINAL) validate
	$(MANAGE) compress --settings=$(APP).settings_production

# run this one the very first time you check
# this out on a new machine to set up dev
# database, etc. You probably *DON'T* want
# to run it after that, though.
install: $(SENTINAL) validate test flake8
	createdb $(APP)
	$(MANAGE) syncdb --noinput
	make migrate

.PHONY: clean collectstatic compress install pull rebase shell validate migrate runserver flake8 test jenkins
