.PHONY: data

data:
	@echo "Pulling data..."
	poetry run dvc pull -r read

experiment:
	@echo "Running experiment..."
	poetry run dvc exp run

test:
	pytest