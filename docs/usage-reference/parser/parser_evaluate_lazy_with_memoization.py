"""EvaluateParser lazy with memoization example."""


import fromconfig

ENVIRONMENT = {"ENV_VAR": "UNINITIALIZED", "N_HEAVY_COMPUTATIONS": 0}

if __name__ == "__main__":

    def initialize_environment():
        ENVIRONMENT["ENV_VAR"] = "VALUE"

    def load_env_var_and_perform_heavy_computations():
        ENVIRONMENT["N_HEAVY_COMPUTATIONS"] += 1
        return ENVIRONMENT["ENV_VAR"]

    def run_job(env_var):
        assert env_var == "VALUE"

    def pipeline(jobs):
        for job in jobs:
            job()

    # We want to configure a job that runs the following
    # >>> initialize_environment()
    # >>> run_job(load_env_var_and_perform_heavy_computations())
    # >>> run_job(load_env_var_and_perform_heavy_computations())
    # where load_env_var_and_perform_heavy_computations is only evaluated once.

    config = {
        "_attr_": "pipeline",
        "_eval_": "partial",
        "jobs": [
            {"_attr_": "initialize_environment", "_eval_": "partial"},
            {
                "_attr_": "run_job",
                "_eval_": "partial",
                "env_var": {
                    "_attr_": "load_env_var_and_perform_heavy_computations",
                    "_eval_": "lazy",
                    "_memoization_key_": "env_var",
                },
            },
            {
                "_attr_": "run_job",
                "_eval_": "partial",
                "env_var": {
                    "_attr_": "load_env_var_and_perform_heavy_computations",
                    "_eval_": "lazy",
                    "_memoization_key_": "env_var",
                },
            },
        ],
    }
    parser = fromconfig.parser.EvaluateParser()
    parsed = parser(config)
    pipeline = fromconfig.fromconfig(parsed)
    pipeline()
    assert ENVIRONMENT["N_HEAVY_COMPUTATIONS"] == 1
