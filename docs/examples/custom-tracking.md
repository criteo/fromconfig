### Custom Tracking with MlFlow <!-- {docsify-ignore} -->

[MlFlow](https://www.mlflow.org) is an open-source platform for the Machine Learning life-cycle.

To install an launch an MlFlow server

```bash
pip install mlflow
mlflow server --port 5000
```

Once the server is up, you can register new runs and log parameters, metrics, and artifacts. Saving the metrics as a run's artifact is a good way to ensure future reproducibility.

A custom command equivalent to `fromconfig` with MlFlow support would look like

```python
import sys
import functools
import logging
import tempfile
import json
from pathlib import Path

import mlflow
import fire
import fromconfig


LOGGER = logging.getLogger(__name__)


def main(
    *paths: str,
    use_mlflow: bool = False,
    run_name: str = None,
    run_id: str = None,
    tracking_uri: str = None,
    experiment_name: str = None,
    artifact_location: str = None,
):
    """Command line with MlFlow support."""
    if not paths:
        return main

    # Load configs and merge them
    configs = [fromconfig.load(path) for path in paths]
    config = functools.reduce(fromconfig.utils.merge_dict, configs)

    # Parse merged config
    parser = fromconfig.parser.DefaultParser()
    parsed = parser(config)

    if use_mlflow:  # Create run, log configs and parameters
        # Configure MlFlow
        if tracking_uri is not None:
            mlflow.set_tracking_uri(tracking_uri)
        if experiment_name is not None:
            if mlflow.get_experiment_by_name(experiment_name) is None:
                mlflow.create_experiment(name=experiment_name, artifact_location=artifact_location)
            mlflow.set_experiment(experiment_name)

        # Start run (cannot use context because of python Fire)
        run = mlflow.start_run(run_id=run_id, run_name=run_name)

        # Log run information
        url = f"{mlflow.get_tracking_uri()}/#/experiments/{run.info.experiment_id}/runs/{run.info.run_id}"
        LOGGER.info(f"MlFlow Run Initialized: {url}")

        # Save merged and parsed config to MlFlow
        dir_artifacts = tempfile.mkdtemp()
        with Path(dir_artifacts, "config.json").open("w") as file:
            json.dump(config, file, indent=4)
        with Path(dir_artifacts, "parsed.json").open("w") as file:
            json.dump(parsed, file, indent=4)
        mlflow.log_artifacts(local_dir=dir_artifacts)

        # Log flattened parameters
        for key, value in fromconfig.utils.flatten(parsed):
            mlflow.log_param(key=key, value=value)

    return fromconfig.fromconfig(parsed)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)  # Print INFO level logs
    sys.path.append(".")  # For local imports
    fire.Fire(main)
```

This example can be found in [`examples/mlflow`](examples/mlflow).

Start an MlFlow server with

```bash
mlflow server --port 5000
```

And submit an experiment with

```bash
python submit.py config.yaml params.yaml \
    --use_mlflow=True \
    --tracking_uri='http://127.0.0.1:5000' \
    --run_name='test' \
    - model - train
```

This should print

```
INFO:__main__:MlFlow Run Initialized: http://127.0.0.1:5000/#/experiments/0/runs/<SOME RUN ID>
Training model with learning_rate 0.1
```

Navigate to the URL to inspect the run's outputs (parameters, configs, metrics, etc.)
