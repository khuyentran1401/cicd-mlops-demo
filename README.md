# Continuous Integration for Machine Learning Models

## Project Structure
* `src`: consists of Python scripts
* `conf`: consists of configuration files
* `data`: consists of data
* `tests`: consists of test files
* `dvclive`: consists of metrics and parameters of DVC experiments

## Set Up the Project
1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Set up the environment:
```bash
# activate the virtual environment
make activate

# install dependencies and pull data from the remote storage 
make setup
```
## Run the Project
```bash
dvc exp run
```




