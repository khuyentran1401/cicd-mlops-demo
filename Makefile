# Delete all compiled Python files
clean:
	find . -maxdepth 1 -type d -name '*cache' -print0 | xargs -0 rm -rf

# Create requirements.txt from requirements.in
requirements.txt: requirements.in
	pip-compile requirements.in --resolver=backtracking

# Specify how to deploy the model
svm-app.mlem: 
	mlem declare deployment flyio svm-app --app_name=svm-mlem  

# Create and version an experiment
experiment:
	dvc exp run train
	git add .
	git commit -m 'Change model'
	git push origin cd-main 

# Change and commit GitHub workflow
workflow:
	git add .
	git commit -m 'Change workflow'
	git push origin cd-main 