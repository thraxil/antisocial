APP=antisocial
REPO=thraxil

MAX_COMPLEXITY=5
JS_FILES = media/js/collections/ media/js/models/ media/js/views media/js/main.js media/js/templates

include *.mk

all: jshint jscs flake8 test
