init:
	pip3 install pipenv --upgrade
	pipenv install --three --skip-lock
	pipenv install --three --skip-lock --dev

test:
	tox

ci:
	pipenv run pytest --cov --cov-config .coveragerc --verbose

lint:
	pipenv run flake8 uberfare tests

coverage:
	codecov

clean:
	rm -rf *.egg-info .eggs dist .pytest_cache .tox
