# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-11-28

### Added
- Custom integration icon support
- Icon configuration via icons.json

## [0.1.0] - 2025-11-28

### Added
- Initial release of GPSLive integration for Home Assistant
- Configuration flow with API key authentication
- Device tracker platform for GPS location tracking
- Sensor platform with three sensor types per device:
  - Odometer sensor (total distance in km)
  - Speed sensor (current speed in km/h)
  - Battery sensor (battery level percentage)
- Support for GPSLive API v1 endpoints
- Automatic device discovery from GPSLive account
- 30-second polling interval for location updates
- Device attributes including:
  - IMEI
  - Plate number
  - Speed
  - Odometer reading
  - Last update timestamp (UTC)
  - Protocol/device type
  - Active status
  - Raw device parameters
- HACS compatibility for easy installation
- Comprehensive error handling for API authentication and connection issues

### Technical Details
- API Base URL: `https://api.gpslive.app`
- Supported API endpoints: `/v1/devices/list`, `/v1/devices`, `/v1/devices/locations`
- Integration type: Cloud Polling
- Minimum Home Assistant version: 2023.1.0

[0.2.0]: https://github.com/BenWolstencroft/home-assistant-gpslive-integration/releases/tag/v0.2.0
[0.1.0]: https://github.com/BenWolstencroft/home-assistant-gpslive-integration/releases/tag/v0.1.0
