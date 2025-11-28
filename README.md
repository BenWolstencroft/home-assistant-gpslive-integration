# GPSLive Integration for Home Assistant

A custom Home Assistant integration for GPSLive GPS tracking devices. This integration provides device tracking and allows you to monitor your GPS devices directly in Home Assistant.

## Features

- 🔐 Easy setup through Home Assistant UI with API key
- 📍 Device tracker entities for all your GPSLive devices
- 🔄 Automatic polling for location updates (every 30 seconds)
- 🔋 Battery level monitoring
- 📊 Additional attributes (speed, heading, altitude, accuracy, timestamp)

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/BenWolstencroft/home-assistant-gpslive-integration`
6. Select category: "Integration"
7. Click "Add"
8. Search for "GPSLive" and install

### Manual Installation

1. Copy the `custom_components/gpslive` folder to your Home Assistant's `custom_components` directory
2. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for **GPSLive**
4. Enter your GPSLive API key
5. Click **Submit**

Your devices will be automatically discovered and added as device tracker entities.

## API Key

To get your GPSLive API key:
1. Log in to your GPSLive account
2. Navigate to your account settings or API section
3. Generate or copy your API key

## Usage

Once configured, your GPS devices will appear as device tracker entities:
- `device_tracker.gpslive_device_name`

You can use these entities in:
- Automations
- Scripts
- Lovelace cards (map, person, etc.)
- Zones

### Example Automation

```yaml
automation:
  - alias: "Notify when device enters home zone"
    trigger:
      - platform: zone
        entity_id: device_tracker.gpslive_my_device
        zone: zone.home
        event: enter
    action:
      - service: notify.mobile_app
        data:
          message: "Device has arrived home"
```

## Entity Attributes

Each device tracker provides the following attributes:
- `latitude` - Current latitude
- `longitude` - Current longitude
- `battery_level` - Battery percentage
- `speed` - Current speed (if available)
- `heading` - Direction of travel (if available)
- `altitude` - Elevation (if available)
- `accuracy` - GPS accuracy in meters (if available)
- `timestamp` - Last update time (if available)

## Troubleshooting

### Connection Issues
- Verify your API key is correct
- Check your internet connection
- Ensure the GPSLive API is accessible

### Devices Not Appearing
- Verify your devices are active in GPSLive
- Check Home Assistant logs for errors
- Try removing and re-adding the integration

## Support

For issues, feature requests, or questions:
- [GitHub Issues](https://github.com/BenWolstencroft/home-assistant-gpslive-integration/issues)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits

Developed by [@BenWolstencroft](https://github.com/BenWolstencroft)
