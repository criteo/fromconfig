# Parser <!-- {docsify-ignore} -->


<a id="default"></a>
## Default

`FromConfig` comes with a default parser which sequentially applies

- [`OmegaConfParser`](#omegaconf): can be practical for interpolation.
- [`ReferenceParser`](#references): resolves references.
- [`EvaluateParser`](#evaluate): syntactic sugar to configure `functool.partial` or simple imports.
- [`SingletonParser`](#singleton): syntactic sugar to define singletons.

For example, let's see how to create singletons, use references and interpolation

[default.py](default.py ':include :type=code python')


<a id="omegaconf"></a>
## OmegaConf

[OmegaConf](https://omegaconf.readthedocs.io) is a YAML based hierarchical configuration system with support for merging configurations from multiple sources. The `OmegaConfParser` wraps some of its functionality (for example, variable interpolation).

For example

[parser_omegaconf.py](parser_omegaconf.py ':include :type=code python')

This examples uses

- interpolation, with `${host}` (it is more powerful than references, since it can be included in strings to format the result as in `"${host}:${port}"`)
- custom interpolation with resolvers `now` and `random_hex`. You can register your own resolvers using the `resolvers` key of the config. The `resolvers` should be a mapping from resolver name to a function, import string or any config dictionary defining a function. Using a resolver is as simple as doing `${resolver_name:arg1,arg2,...}`.


The following resolvers are available by default

- `env`: retrieves the value of environment variables. For example `${env:USER}` evaluates to the `$USER` environment variable
- `now`: generates the current date with `datetime.now().strftime(fmt)` where `fmt` can be provided as an argument, and defaults to `%Y-%m-%d-%H-%M-%S`.

Learn more on the [OmegaConf documentation website](https://omegaconf.readthedocs.io).


<a id="references"></a>
## References

To make it easy to compose different configuration files and avoid deeply nested config dictionaries, you can use the `ReferenceParser`.

For example,

[parser_reference_simple.py](parser_reference_simple.py ':include :type=code python')

The `ReferenceParser` looks for values starting with a `@`, then split by `.`, and navigate from the top-level dictionary. It then copies the resolved reference in place of the `@reference` string.

In practice, it makes configuration files more readable (flat).

It is also a convenient way to dynamically compose different configs.

For example

[parser_reference_full.py](parser_reference_full.py ':include :type=code python')

It is also important to know that __the reference are only copies at the config level__. When instantiating the full config dictionary, you may end up with multiple instances configured in the same way.

If you wish to instantiate only one instance, be explicit and use the [`SingletonParser`](#singleton).

<a id="evaluate"></a>
## Evaluate

The `EvaluateParser` makes it possible to simply import a class / function, or configure a constructor via a `functools.partial` call.

The parser uses a special key `_eval_` with possible values

__call__

Standard behavior, results in `attr(kwargs)`.

For example,

[parser_evaluate_call.py](parser_evaluate_call.py ':include :type=code python')

__partial__

Delays the call, results in a `functools.partial(attr, **kwargs)`.

For example,

[parser_evaluate_partial.py](parser_evaluate_partial.py ':include :type=code python')

__import__

Simply import the attribute, results in `attr`.

For example,

[parser_evaluate_import.py](parser_evaluate_import.py ':include :type=code python')


<a id="singleton"></a>
## Singleton

To define singletons (typically an object used in multiple places), use the `SingletonParser`.

For example,

[parser_singleton.py](parser_singleton.py ':include :type=code python')

Without the `_singleton_` entry, two different dictionaries would have been created.

Note that using references is not a solution to create singletons, as the reference mechanism only copies missing parts of the configs.

The parser uses the special key `_singleton_` whose value is the name associated with the instance to resolve singletons at instantiation time.
