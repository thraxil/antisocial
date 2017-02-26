APP=antisocial
REPO=thraxil

MAX_COMPLEXITY=5
JS_FILES = media/js/src

include *.mk

all: jshint jscs flake8 test
