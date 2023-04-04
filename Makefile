## Delete all compiled Python files
clean:
	find . -maxdepth 1 -type d -name '*cache' -print0 | xargs -0 rm -rf