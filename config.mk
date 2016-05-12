# default config values that can all be overridden
VE ?= ./ve
MANAGE ?= ./manage.py
FLAKE8 ?= $(VE)/bin/flake8
SYS_PYTHON ?= python
PIP ?= $(VE)/bin/pip
SENTINAL ?= $(VE)/sentinal
WHEEL_VERSION ?= 0.24.0
REQUIREMENTS ?= requirements.txt
VIRTUALENV ?= virtualenv.py
SUPPORT_DIR ?= requirements/virtualenv_support/
WHEELHOUSE ?= wheelhouse

JS_FILES ?= media/js/

ifeq ($(TAG), undefined)
	IMAGE ?= $(REPO)/$(APP)
else
	IMAGE ?= $(REPO)/$(APP):$(TAG)
endif

MAX_COMPLEXITY ?= 10

