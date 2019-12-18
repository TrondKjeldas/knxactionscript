
.PHONY: test
test:
	coverage run -m unittest discover -s test/

clean:
	rm -Rf dist build
