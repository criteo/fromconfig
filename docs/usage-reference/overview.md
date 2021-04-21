# Overview <!-- {docsify-ignore} -->

The library is made of three main components.

1. A independent and lightweight __syntax__ to instantiate any Python object from dictionaries with `fromconfig.fromconfig(config)` (using special keys `_attr_` and `_args_`). See [fromconfig](usage-reference/fromconfig/).
2. A simple abstraction to parse configs before instantiation. This allows configs to remain short and readable with syntactic sugar to define singletons, perform interpolation, etc. See [Parser](usage-reference/parser/).
3. A composable, flexible, and customizable framework to manipulate configs and launch jobs on remote servers, log values to tracking platforms, etc. See [Launcher](usage-reference/launcher/).

The [Command Line](usage-reference/command-line) combines these three components for ease of use.
