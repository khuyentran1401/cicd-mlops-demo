# Continuous Integration for Machine Learning Models

This is a sample project that showcases how to use CI for machine learning models.

## Why?
Continuous Integration (CI) is the practice of continuously merging and testing code changes into a shared repository. In a machine learning project, CI can be very useful for several reasons:

- Catching errors early: With CI, any changes made to the codebase are automatically built and tested, which helps catch any errors early in the development cycle. This is especially important in machine learning projects since models can be complex, and errors can be hard to spot.

- Ensuring reproducibility: With CI, you can ensure that the codebase is always in a reproducible state. This means that anyone can run the code at any time and get the same results. This is important in machine learning projects because reproducibility is essential for scientific research.

- Facilitating collaboration: With CI, everyone on the team is working with the same codebase, and everyone can see changes made by other team members. This can help prevent conflicts and facilitate collaboration.

- Automating tests: CI tools can automatically run tests on the codebase, ensuring that everything is working as expected. This can help catch errors that might otherwise go unnoticed.

- Ensuring scalability: Machine learning projects often involve large datasets and complex models. With CI, you can ensure that the codebase is scalable and can handle large datasets and models.

## Scenario
- Data scientists make some changes to the code and create a new model locally
- Data scientists push model and data to S3
- Data scientists create a pull request for the changes
- A CI pipeline is kicked off to test the data and model

## Pipeline overview
- Pull data and model from a remote storage
- Run tests
- Automatically generate metrics report (optional)
- If all tests passed, the code is merged to the main branch

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

## Try it out
To try out this project, first start with cloning the project to your local machine:
```bash
git clone https://github.com/khuyentran1401/cicd-mlops-demo
```

Next, setup the environment by following these steps:
1. Install [Poetry](https://python-poetry.org/docs/#installation)
2. Set up the environment:
```bash
# Install dependencies
poetry install --without dev

# Pull data from the remote storage 
make data
```

Make changes to any files in the following directories `src`, `tests`, `conf`. To demonstrate, we will make minor changes the file `conf/config.yaml`:

![](demo_images/code_change.png)

Create an experiment:
```bash
make experiment
```

Add, commit, and push changes to the repository:

```bash
git add .
git commit -m 'change process_3 to process_1'
git push origin main
```

Create a pull request and a GitHub job will be triggered:

![](demo_images/pr.png)




