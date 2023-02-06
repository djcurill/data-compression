activate-env:
	source .venv/bin/activate

deactivate-env:
	deactivate
	
test:
	pytest

run:
	python3 -m src.main