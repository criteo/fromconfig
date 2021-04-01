"""Hyper Parameter search example."""

import fromconfig


if __name__ == "__main__":
    config = {
        "model": {"_attr_": "ml.Model", "dim": "@params.dim"},
        "optimizer": {"_attr_": "ml.Optimizer", "learning_rate": "@params.learning_rate"},
        "trainer": {"_attr_": "ml.Trainer", "model": "@model", "optimizer": "@optimizer"},
    }
    parser = fromconfig.parser.DefaultParser()
    for dim in [10, 100]:
        for learning_rate in [0.01, 0.1]:
            params = {"dim": dim, "learning_rate": learning_rate}
            parsed = parser({**config, "params": params})
            trainer = fromconfig.fromconfig(parsed)["trainer"]
            trainer.run()
            # Clear the singletons if any as we most likely don't want
            # to share between configs
            fromconfig.parser.singleton.clear()
