# Parser <!-- {docsify-ignore} -->


<a id="default"></a>
## Default

`FromConfig` comes with a default parser which sequentially applies

- [`OmegaConfParser`](#omegaconf): can be practical for interpolation.
- [`EvaluateParser`](#evaluate): syntactic sugar to configure `functool.partial` or simple imports.
- [`SingletonParser`](#singleton): syntactic sugar to define singletons.

For example, let's see how to create singletons and use interpolation.

[default.py](default.py ':include :type=code python')


<a id="omegaconf"></a>
## OmegaConf

[OmegaConf](https://omegaconf.readthedocs.io) is a YAML based hierarchical configuration system with support for merging configurations from multiple sources. The `OmegaConfParser` wraps some of its functionality (for example, variable interpolation).

For example

[parser_omegaconf.py](parser_omegaconf.py ':include :type=code python')

This examples uses

- interpolation, with `${host}`
- custom interpolation with resolvers `now` and `random_hex`. You can register your own resolvers using the `resolvers` key of the config. The `resolvers` should be a mapping from resolver name to a function, import string or any config dictionary defining a function. Using a resolver is as simple as doing `${resolver_name:arg1,arg2,...}`.


The following resolvers are available by default

- `env`: retrieves the value of environment variables. For example `${env:USER}` evaluates to the `$USER` environment variable
- `now`: generates the current date with `datetime.now().strftime(fmt)` where `fmt` can be provided as an argument, and defaults to `%Y-%m-%d-%H-%M-%S`.

Learn more on the [OmegaConf documentation website](https://omegaconf.readthedocs.io).

<a id="evaluate"></a>
## Evaluate

The `EvaluateParser` makes it possible to simply import a class / function, or configure a constructor via a `functools.partial` call.

The parser uses a special key `_eval_` with possible values

__call__

Standard behavior, results in `attr(kwargs)`.

For example,

[parser_evaluate_call.py](parser_evaluate_call.py ':include :type=code python')

__import__

Simply import the attribute, results in `attr`.

For example,

[parser_evaluate_import.py](parser_evaluate_import.py ':include :type=code python')

__partial__

Delays the call, results in a `functools.partial(attr, *args, **kwargs)`.

For example,

[parser_evaluate_partial.py](parser_evaluate_partial.py ':include :type=code python')

It is also possible to delay the call to the function argument if you want them to be evaluated at run time rather
than when the configuration is parsed.

[parser_evaluate_lazy.py](parser_evaluate_lazy.py ':include :type=code python')

<a id="singleton"></a>
## Singleton

To define singletons (typically an object used in multiple places), use the `SingletonParser`.

For example,

[parser_singleton.py](parser_singleton.py ':include :type=code python')

Without the `_singleton_` entry, two different dictionaries would have been created.

Note that using interpolation is not a solution to create singletons, as the interpolation mechanism only copies missing parts of the configs.

The parser uses the special key `_singleton_` whose value is the name associated with the instance to resolve singletons at instantiation time.
