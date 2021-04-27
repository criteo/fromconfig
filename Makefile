install: ## [Local development] Upgrade pip, install requirements, install package.
	python -m pip install -U pip setuptools wheel
	python -m pip install -r requirements.txt
	python -m pip install -e .

serve-doc: ## [Documentation] Serve documentation on http://localhost:3000
	cd docs && python -m http.server 3000

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
	cd docs/getting-started/quickstart && fromconfig config.yaml params.yaml - model - train
	cd docs/getting-started/quickstart && python manual.py
	cd docs/getting-started/cheat-sheet && fromconfig config.yaml launcher.yaml - model - train
	cd docs/examples/manual-parsing  && python manual.py
	cd docs/examples/hyper-params && fromconfig config.yaml hparams.yaml - model - train
	cd docs/examples/hyper-params && python hp.py
	cd docs/examples/change-parser && fromconfig config.yaml launcher.yaml - model - train
	cd docs/examples/configure-launcher && fromconfig config.yaml --launcher.run=dry - model - train
	cd docs/examples/configure-launcher && fromconfig config.yaml launcher_dry.yaml - model - train
	cd docs/examples/configure-launcher && fromconfig config.yaml --logging.level=20 --logging.log_config=False - model - train
	cd docs/examples/configure-launcher && fromconfig config.yaml launcher_logging.yaml - model - train
	cd docs/examples/machine-learning && fromconfig trainer.yaml model.yaml optimizer.yaml params/small.yaml - trainer - run
	cd docs/examples/machine-learning && fromconfig trainer.yaml model.yaml optimizer.yaml params/big.yaml - trainer - run
	cd docs/examples/combine-configs && fromconfig config.yaml params/small.yaml - trainer - run
	cd docs/examples/combine-configs && fromconfig config.yaml params/big.yaml - trainer - run
	cd docs/examples/combine-configs && python convert.py trainer.yaml trainer.json
	cd docs/usage-reference/fromconfig && python example.py
	cd docs/usage-reference/fromconfig && python example_kwargs.py
	cd docs/usage-reference/parser && python default.py
	cd docs/usage-reference/parser && python parser_evaluate_call.py
	cd docs/usage-reference/parser && python parser_evaluate_import.py
	cd docs/usage-reference/parser && python parser_evaluate_partial.py
	cd docs/usage-reference/parser && python parser_omegaconf.py
	cd docs/usage-reference/parser && python parser_singleton.py
	cd docs/usage-reference/launcher && fromconfig config.yaml hparams.yaml launcher.yaml - model - train
	cd docs/usage-reference/launcher && fromconfig --hparams.a=1,2 --hparams.b=3,4
	cd docs/development/custom-fromconfig && python config.py
	cd docs/development/custom-fromconfig && python custom.py
	cd docs/development/custom-parser && python lorem_ipsum.py
	cd docs/development/custom-launcher && fromconfig config.yaml launcher.yaml - model - train
	cd docs/extensions && python -m pip install -r requirements.txt
	cd docs/extensions/mlflow && fromconfig config.yaml params.yaml launcher.yaml - model - train
	cd docs/extensions/mlflow && fromconfig config.yaml params.yaml --launcher.log=logging,mlflow --logging.level=20 - model - train
	cd docs/extensions/mlflow && fromconfig config.yaml params.yaml launcher_advanced.yaml - model - train
	cd docs/extensions/yarn && python monkeypatch_fromconfig.py config.yaml params.yaml launcher.yaml - model - train
	cd docs/extensions/yarn && python monkeypatch_fromconfig.py config.yaml params.yaml --launcher.run=yarn - model - train
	cd docs/extensions/hparams-yarn-mlflow && python monkeypatch_fromconfig.py config.yaml hparams.yaml launcher.yaml - model - train

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
