# Continuous Integration for a Machine Learning Model

## Project Structure
* `src`: consists of Python scripts
* `conf`: consists of configuration files
* `data`: consists of data
* `tests`: consists of test files

## Set Up the Project
1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Set up the environment:
```bash
make setup
make install_all
```
3. To persist the output of Prefect's flow, run 
```bash
export PREFECT__FLOWS__CHECKPOINTING=true
```

## Run the Project
To run all flows, type:
```bash
python src/main.py
```

To run the `process` flow, type:
```bash
python src/main.py flow=process
```

To run the `segment` flow, type:
```bash
python src/main.py flow=segment
```




