# Why FromConfig ? <!-- {docsify-ignore} -->

`fromconfig` enables the instantiation of arbitrary trees of Python objects from config files.

It echoes the `FromParams` base class of [AllenNLP](https://github.com/allenai/allennlp).

It is particularly well suited for __Machine Learning__. Launching training jobs on remote clusters requires custom command lines, with arguments that need to be propagated through the call stack (e.g., setting parameters of a particular layer). The usual way is to write a custom command with a reduced set of arguments, combined by an assembler that creates the different objects. With `fromconfig`, the command line becomes generic, and all the specifics are kept in config files. As a result, this preserves the code from any backwards dependency issues and allows full reproducibility by saving config files as jobs' artifacts. It also makes it easier to merge different sets of arguments in a dynamic way through references and interpolation.

`fromconfig` is based off the config system developed as part of the [deepr](https://github.com/criteo/deepr) library, a collections of utilities to define and train Tensorflow models in a Hadoop environment.

Other relevant libraries are:

* [fire](https://github.com/google/python-fire) automatically generate command line interface (CLIs) from absolutely any Python object.
* [omegaconf](https://github.com/omry/omegaconf) YAML based hierarchical configuration system with support for merging configurations from multiple sources.
* [hydra](https://hydra.cc/docs/intro/) A higher-level framework based off `omegaconf` to configure complex applications.
* [gin](https://github.com/google/gin-config) A lightweight configuration framework based on dependency injection.
* [thinc](https://thinc.ai/) A lightweight functional deep learning library that comes with an integrated config system
