# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org).


## [0.5.0] - 2021-04-30

### Added
- `NAME` support in extensions for multiple launchers.
- Better header in `hparams`

### Changed
- Order of steps in `DefaultLauncher` is now `sweep, log, parse, run`.

### Deprecated
### Removed
- `log_config` in logging launcher.

### Fixed
### Security



## [0.4.1] - 2021-04-28

### Added
- The `_attr_` key can be used with an extension name in `Launcher.fromconfig`.

### Changed
- The `fromconfig` method of the `FromConfig` base class signature is now generic (`config` does not have to be a Mapping).
- The `Parser` `__call__` signature is also more generic (accepts `Any` instead of `Mapping`)

### Deprecated
### Removed
- The steps syntax in `Launcher.fromconfig` is now in `DefaultLauncher`

### Fixed
- Better type handling for the `OmegaConfParser` (only attempts to find resolvers if `config` is a mapping)

### Security



## [0.4.0] - 2021-04-27

### Added
### Changed
### Deprecated
### Removed
- `ReferenceParser`: less powerful than the `OmegaConfParser` but same functionality, only caused confusion.

### Fixed
### Security


## [0.3.3] - 2021-04-23

### Added
- Improved error message when trying to reload a `.jsonnet` file but `jsonnet` is not installed.
- include `!include` and merge `<<:` support for YAML files
- Custom resolvers easy registration for `OmegaConfParser`
- Default resolver `now` for `OmegaConf`

### Changed
- `jsonnet` import does not log an error if jsonnet is not available.

### Deprecated
### Removed
### Fixed
### Security


## [0.3.2] - 2021-04-22

### Added
### Changed
### Deprecated
### Removed
### Fixed
- docs/README.md must be in data files in setup.py

### Security


## [0.3.1] - 2021-04-21

### Added
- `DryLauncher` to dry-run config.
- Skip launcher instantiation if config is `None`

### Changed
### Deprecated
### Removed
### Fixed
- Wrong order when merging configs in `cli.main`

### Security


## [0.3.0] - 2021-04-20

### Added
- `Launcher` base class with `HParamsLauncher`, `ParserLauncher`, `LoggingLauncher` and `LocalLauncher`
- CLI mechanism for argument parsing and `fire.Fire` integration (now in Launcher)
- Overrides support via key-value parameters for the CLI thanks to `utils.expand`
- `ChainParser` to easily chain parsers.

### Changed
- The `FromConfig` class now has a default implementation of `fromconfig`
- The `DefaultParser` now inherits `ChainParser` and its implementation is moved to `parser/default.py`

### Deprecated
### Removed
- `jsonnet` requirement in the setup.py (it should be optional as it tends to cause issues in some users).

### Fixed
### Security



## [0.2.2] - 2021-03-31

### Added
### Changed
- `fromconfig.Config` now inherits `dict` instead of `collections.UserDict` to support JSON serialization.

### Deprecated
### Removed
### Fixed
### Security


## [0.2.0] - 2021-03-18

### Added
### Changed
- Improved readme

### Deprecated
### Removed
### Fixed
### Security

## [0.1.0] - 2021-03-18

### Added
- Initial commit

### Changed
### Deprecated
### Removed
### Fixed
### Security
