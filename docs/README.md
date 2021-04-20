# FromConfig

[![pypi](https://img.shields.io/pypi/v/fromconfig.svg)](https://pypi.python.org/pypi/fromconfig)
[![ci](https://github.com/criteo/fromconfig/workflows/Continuous%20integration/badge.svg)](https://github.com/criteo/fromconfig/actions?query=workflow%3A%22Continuous+integration%22)

A library to instantiate any Python object from configuration files.

Thanks to [Python Fire](https://github.com/google/python-fire), `fromconfig` acts as a generic command line interface from configuration files *with absolutely no change to the code*.

What are `fromconfig` strengths?

1. __No code change__ Install with `pip install fromconfig` and [get started](#quickstart).
2. __Simplicity__ See the simple [config syntax](#config-syntax) and [command line](#command-line).
3. __Extendability__ See how to write [a custom `Parser`](#custom-parser), [a custom `Launcher`](#custom-launcher), and [a custom `FromConfig` class](#custom-fromconfig).


![FromConfig](https://raw.githubusercontent.com/criteo/fromconfig/master/docs/images/fromconfig.svg)


The `fromconfig` library relies on three components.

1. A independent and lightweight __syntax__ to instantiate any Python object from dictionaries with `fromconfig.fromconfig(config)` (using special keys `_attr_` and `_args_`) (see [Config Syntax](#config-syntax)).
2. A composable, flexible, and customizable framework to manipulate configs and launch jobs on remote servers, log values to tracking platforms, etc. (see [Launcher](#launcher)).
3. A simple abstraction to parse configs before instantiation. This allows configs to remain short and readable with syntactic sugar to define singletons, perform interpolation, etc. (see [Parser](#parsing)).
