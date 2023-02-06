SHELL := /bin/bash
PROB=0.9
SIZE=100
	
test:
	pytest

run-example:
	python3 -m src.main --fixed=True

run-experiment:
	python3 -m src.main --size=$(SIZE) --prob=$(PROB) --fixed=False