# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org).


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
