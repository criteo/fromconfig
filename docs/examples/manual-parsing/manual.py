"""Manual Parsing Example."""

import functools

import fromconfig

import model


if __name__ == "__main__":
    # Load configs from yaml and merge into one dictionary
    paths = ["config.yaml", "params.yaml"]
    configs = [fromconfig.load(path) for path in paths]
    config = functools.reduce(fromconfig.utils.merge_dict, configs)

    # Parse the config (resolve interpolation)
    parser = fromconfig.parser.DefaultParser()
    parsed = parser(config)

    # Instantiate one of the keys
    instance = fromconfig.fromconfig(parsed["model"])
    assert isinstance(instance, model.Model)
    instance.train()

    # You can also use the DefaultLauncher that replicates the CLI
    launcher = fromconfig.launcher.DefaultLauncher()
    launcher(config, "model - train")
