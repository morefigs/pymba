# Pymba change log

## [0.3.7] - 2020-06-16
### Added
- Ancillary data and feature invalidation functions.
- Manual setting of frame payload size.

## [0.3.6] - 2019-09-11
### Added
- NumPy support for (most) pixel formats.

## [0.3.5] - 2019-06-07
### Added
- Support for Vimba v3.0+.

## [0.3.4] - 2019-04-13
### Added
- Timeout error checking to single frame acquisition example. 
### Changed
- Removed f-strings for backwards compatibility.

## [0.3.3] - 2019-03-28
### Added
- Timeout parameter to acquire frame function.
### Changed
- MIT license.
### Fixed
- Bug fix for USB cameras trying to adjust packet size.

## [0.3.2] - 2019-03-09
### Added
- Colour camera example.
- Bug fix when attempting to open a USB camera.

## [0.3.1] - 2019-02-21
### Added
- Auto adjust packet size upon opening camera.
- Command type features can now be called directly as an object attribute.
### Changed
- Increased default frame buffer size from 3 to 10.
- Also looks in working directory for VimbaC.dll to make distribution easier.

## [0.3] - 2019-02-11
### Added
- Convenience functions for arming and acquiring single images and image streams from a camera.

## [0.2] - 2019-01-30
### Changed
- Refactored classes and module structure.
- Python 3 support only.
### Added
- Usage examples.
