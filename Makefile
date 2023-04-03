.PHONY: data

data:
	@echo "Pulling data..."
	poetry run dvc pull -r read

experiment:
	@echo "Running experiment..."
	poetry run dvc exp run

push_data:
	@echo "Pushing data and model..."
	poetry run dvc push -r read-write

test:
	pytest

## Delete all compiled Python files
clean:
	find . -maxdepth 1 -type d -name '*cache' -print0 | xargs -0 rm -rf