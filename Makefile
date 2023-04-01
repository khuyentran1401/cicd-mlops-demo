activate:
	@echo "Activating virtual environment"
	poetry shell

install: 
	@echo "Installing..."
	poetry install

pull_data:
	@echo "Pulling data..."
	dvc pull -r write

setup: install pull_data

test:
	pytest