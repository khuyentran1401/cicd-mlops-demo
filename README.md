# Continuous Integration for Machine Learning Models

## Tools Used in This Project
* [hydra](https://hydra.cc/): Manage configuration files - [article](https://towardsdatascience.com/introduction-to-hydra-cc-a-powerful-framework-to-configure-your-data-science-projects-ed65713a53c6)
* [pre-commit plugins](https://pre-commit.com/): Automate code reviewing formatting  - [article](https://towardsdatascience.com/4-pre-commit-plugins-to-automate-code-reviewing-and-formatting-in-python-c80c6d2e9f5?sk=2388804fb174d667ee5b680be22b8b1f)
* [poetry](https://python-poetry.org/): Manage Python dependencies - [article](https://towardsdatascience.com/how-to-effortlessly-publish-your-python-package-to-pypi-using-poetry-44b305362f9f)
* [DVC](https://dvc.org/): Version data and experiments - [article](https://towardsdatascience.com/introduction-to-dvc-data-version-control-tool-for-machine-learning-projects-7cb49c229fe0)

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




