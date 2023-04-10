## Delete all compiled Python files
clean:
	find . -maxdepth 1 -type d -name '*cache' -print0 | xargs -0 rm -rf

## Create requirements.txt from requirements.in
requirements.txt: requirements.in
	pip-compile requirements.in --resolver=backtracking