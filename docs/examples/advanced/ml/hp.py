"""Hyper Parameter search example."""

import fromconfig


if __name__ == "__main__":
    config = {
        "model": {"_attr_": "ml.Model", "dim": "@params.dim"},
        "optimizer": {"_attr_": "ml.Optimizer", "learning_rate": "@params.learning_rate"},
        "trainer": {"_attr_": "ml.Trainer", "model": "@model", "optimizer": "@optimizer"},
    }
    parser = fromconfig.parser.DefaultParser()
    params = {"dim": [10, 100, 1000], "learning_rate": [0.001, 0.01, 0.1]}
    for dim in [10, 100, 1000]:
        for learning_rate in [0.001, 0.01, 0.1]:
            config["params"] = {"dim": dim, "learning_rate": learning_rate}
            parsed = parser(config)
            trainer = fromconfig.fromconfig(parsed)["trainer"]
            trainer.run()
