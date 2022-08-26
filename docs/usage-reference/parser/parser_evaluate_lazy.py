"""EvaluateParser lazy example."""

import fromconfig

ENVIRONMENT = {"ENV_VAR": "UNINITIALIZED"}

if __name__ == "__main__":

    def initialize_environment():
        ENVIRONMENT["ENV_VAR"] = "VALUE"

    def load_env_var():
        return ENVIRONMENT["ENV_VAR"]

    def run_job(env_var):
        assert env_var == "VALUE"

    def pipeline(jobs):
        for job in jobs:
            job()

    # We want to configure a job that runs the following
    # >>> initialize_environment()
    # >>> run_job(load_env_var())
    # without changing the function signatures

    config = {
        "_attr_": "pipeline",
        "_eval_": "partial",
        "jobs": [
            {"_attr_": "initialize_environment", "_eval_": "partial"},
            {"_attr_": "run_job", "_eval_": "partial", "env_var": {"_attr_": "load_env_var", "_eval_": "lazy"}},
        ],
    }
    parser = fromconfig.parser.EvaluateParser()
    parsed = parser(config)
    pipeline = fromconfig.fromconfig(parsed)
    pipeline()
