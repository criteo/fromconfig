# FromConfig

[![pypi](https://img.shields.io/pypi/v/fromconfig.svg)](https://pypi.python.org/pypi/fromconfig)
[![ci](https://github.com/criteo/fromconfig/workflows/Continuous%20integration/badge.svg)](https://github.com/criteo/fromconfig/actions?query=workflow%3A%22Continuous+integration%22)

A library to instantiate any Python object from configuration files.

Thanks to [Python Fire](https://github.com/google/python-fire), `fromconfig` acts as a generic command line interface from configuration files *with absolutely no change to the code*.

What are `fromconfig` strengths?

1. __No code change__ Install with `pip install fromconfig` and [get started](getting-started/quickstart).
2. __Simplicity__ See the simple [config syntax](usage-reference/config-syntax) and [command line](usage-reference/command-line).
3. __Extendability__ See how to write [a custom `Parser`](examples/custom-parser), [a custom `Launcher`](examples/custom-launcher), and [a custom `FromConfig` class](examples/custom-fromconfig).


![FromConfig](https://raw.githubusercontent.com/criteo/fromconfig/master/docs/images/fromconfig.svg)
