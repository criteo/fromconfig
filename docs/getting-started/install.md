# Install <!-- {docsify-ignore} -->

## Install with pip

```bash
pip install fromconfig
```

## Install from source

To install the library from source in editable mode

```bash
git clone https://github.com/criteo/fromconfig
cd fromconfig
make install
```

## Optional dependencies

If you want to support the [JSONNET](https://jsonnet.org) format, you need to install it explicitly (it is not included in `fromconfig`s requirements).

First, make sure `JSONNET` is installed on your machine.

With Homebrew

```bash
brew install jsonnet
```

Install the python binding with

```bash
pip install jsonnet
```

See [the official install instructions on GitHub](https://github.com/google/jsonnet).
