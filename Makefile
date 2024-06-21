PACKAGE := datalearn
VERSION := $(shell cat version.py | sed -n -E 's/^__version__ = "(.+?)"/\1/p')

format:
	isort datalearn tests
	yapf --in-place --recursive datalearn tests
