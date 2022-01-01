PYTEST = pytest
TEST = test.py

test: 
	$(PYTEST) $(TEST)
	make clean
clean:
	rm -r __pycache__
	rm -r ../__pycache__
	rm -r .pytest_cache