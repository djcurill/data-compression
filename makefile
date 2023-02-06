PROB=0.9
SIZE=100

activate-env:
	source .venv/bin/activate

deactivate-env:
	deactivate
	
test:
	pytest

run-example:
	python3 -m src.main --fixed=True

run-experiment:
	python3 -m src.main --size=$(SIZE) --prob=$(PROB) --fixed=False