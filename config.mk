# default config values that can all be overridden
VE ?= ./ve
MANAGE ?= ./manage.py
FLAKE8 ?= $(VE)/bin/flake8
SYS_PYTHON ?= python3
PIP ?= $(VE)/bin/pip3
SENTINAL ?= $(VE)/sentinal
WHEEL_VERSION ?= 0.29.0
REQUIREMENTS ?= requirements.txt
VIRTUALENV ?= virtualenv.py
SUPPORT_DIR ?= requirements/virtualenv_support/
WHEELHOUSE ?= wheelhouse
TAG ?= latest

JS_FILES ?= media/js/

IMAGE ?= $(REPO)/$(APP):$(TAG)

MAX_COMPLEXITY ?= 10

