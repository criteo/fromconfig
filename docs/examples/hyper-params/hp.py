"""Manual Hyper Parameter search example."""

import fromconfig


if __name__ == "__main__":
    config = fromconfig.load("config.yaml")
    parser = fromconfig.parser.DefaultParser()
    for learning_rate in [0.01, 0.1]:
        params = {"learning_rate": learning_rate}
        parsed = parser({**config, "hparams": params})
        model = fromconfig.fromconfig(parsed["model"])
        model.train()
        # Clear the singletons if any as we most likely don't want
        # to share between configs
        fromconfig.parser.singleton.clear()
