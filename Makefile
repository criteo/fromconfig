install: ## [Local development] Upgrade pip, install requirements, install package.
	python -m pip install -U pip setuptools wheel
	python -m pip install -r requirements.txt
	python -m pip install -e .

install-dev: ## [Local development] Install test requirements
	python -m pip install -r requirements-test.txt

lint: ## [Local development] Run mypy, pylint and black
	python -m mypy fromconfig
	python -m pylint fromconfig
	python -m black --check -l 120 fromconfig

black: ## [Local development] Auto-format python code using black
	python -m black -l 120 .

test: ## [Local development] Run unit tests, doctest and notebooks
	python -m pytest -v --cov=fromconfig --cov-report term-missing --cov-fail-under 95 tests/unit
	python -m pytest --doctest-modules -v fromconfig
	$(MAKE) examples

examples:  ## [Doc] Run all examples
	cd docs/examples/cheat_sheet && fromconfig config.yaml - model - train
	cd docs/examples/custom_launcher && fromconfig config.yaml launcher.yaml - model - train
	cd docs/examples/custom_parser && python lorem_ipsum.py
	cd docs/examples/launcher && fromconfig config.yaml params.yaml launcher.yaml - model - train
	cd docs/examples/manual && python manual.py
	cd docs/examples/ml && fromconfig trainer.yaml model.yaml optimizer.yaml hparams.yaml - trainer - run
	cd docs/examples/ml && fromconfig trainer.yaml model.yaml optimizer.yaml params/big.yaml - trainer - run
	cd docs/examples/ml && fromconfig trainer.yaml model.yaml optimizer.yaml params/small.yaml - trainer - run
	cd docs/examples/ml && python hp.py
	cd docs/examples/mlflow && python -m pip install mlflow && python submit.py config.yaml params.yaml --use_mlflow=True - model - train
	cd docs/examples/quickstart && fromconfig config.yaml params.yaml - model - train
	cd docs/examples/quickstart && fromconfig config.yaml params.yaml --params.learning_rate=0.01 - model - train

venv-lint-test: ## [Continuous integration] Install in venv and run lint and test
	python3.6 -m venv .env && . .env/bin/activate && make install install-dev lint test && rm -rf .env

build-dist: ## [Continuous integration] Build package for pypi
	python3.6 -m venv .env
	. .env/bin/activate && pip install -U pip setuptools wheel
	. .env/bin/activate && python setup.py sdist
	rm -rf .env

.PHONY: help

help: # Run `make help` to get help on the make commands
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
