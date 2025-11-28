"""Support for GPSLive sensors."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfLength,
    UnitOfSpeed,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up GPSLive sensors based on a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    
    entities = []
    for device in coordinator.data:
        imei = device.get("imei")
        # Add odometer sensor
        entities.append(GPSLiveOdometerSensor(coordinator, device, imei))
        # Add speed sensor
        entities.append(GPSLiveSpeedSensor(coordinator, device, imei))
        # Add battery sensor if available in params
        if params := device.get("params"):
            if isinstance(params, dict) and ("battery" in params or "power" in params):
                entities.append(GPSLiveBatterySensor(coordinator, device, imei))
    
    async_add_entities(entities)


class GPSLiveSensorBase(CoordinatorEntity, SensorEntity):
    """Base class for GPSLive sensors."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        device: dict[str, Any],
        imei: str,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._device = device
        self._imei = imei

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information about this entity."""
        return {
            "identifiers": {(DOMAIN, self._imei)},
            "name": self._device.get("name", f"GPSLive {self._device.get('plateNumber', self._imei)}"),
            "manufacturer": "GPSLive",
            "model": self._device.get("protocol", "GPS Tracker"),
        }

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Find updated device data by IMEI
        for device in self.coordinator.data:
            if device.get("imei") == self._imei:
                self._device = device
                break
        
        super()._handle_coordinator_update()


class GPSLiveOdometerSensor(GPSLiveSensorBase):
    """Representation of a GPSLive odometer sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        device: dict[str, Any],
        imei: str,
    ) -> None:
        """Initialize the odometer sensor."""
        super().__init__(coordinator, device, imei)
        self._attr_unique_id = f"gpslive_{imei}_odometer"
        self._attr_name = f"{device.get('name', 'Device')} Odometer"
        self._attr_device_class = SensorDeviceClass.DISTANCE
        self._attr_state_class = SensorStateClass.TOTAL_INCREASING
        self._attr_native_unit_of_measurement = UnitOfLength.KILOMETERS
        self._attr_icon = "mdi:counter"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        odometer = self._device.get("odometer")
        if odometer is not None:
            # Convert to kilometers if needed (API returns in km)
            return round(float(odometer), 2)
        return None


class GPSLiveSpeedSensor(GPSLiveSensorBase):
    """Representation of a GPSLive speed sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        device: dict[str, Any],
        imei: str,
    ) -> None:
        """Initialize the speed sensor."""
        super().__init__(coordinator, device, imei)
        self._attr_unique_id = f"gpslive_{imei}_speed"
        self._attr_name = f"{device.get('name', 'Device')} Speed"
        self._attr_device_class = SensorDeviceClass.SPEED
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = UnitOfSpeed.KILOMETERS_PER_HOUR
        self._attr_icon = "mdi:speedometer"

    @property
    def native_value(self) -> float | None:
        """Return the state of the sensor."""
        speed = self._device.get("speed")
        if speed is not None:
            return round(float(speed), 1)
        return None


class GPSLiveBatterySensor(GPSLiveSensorBase):
    """Representation of a GPSLive battery sensor."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        device: dict[str, Any],
        imei: str,
    ) -> None:
        """Initialize the battery sensor."""
        super().__init__(coordinator, device, imei)
        self._attr_unique_id = f"gpslive_{imei}_battery"
        self._attr_name = f"{device.get('name', 'Device')} Battery"
        self._attr_device_class = SensorDeviceClass.BATTERY
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_native_unit_of_measurement = "%"
        self._attr_icon = "mdi:battery"

    @property
    def native_value(self) -> int | None:
        """Return the state of the sensor."""
        if params := self._device.get("params"):
            if isinstance(params, dict):
                battery = params.get("battery") or params.get("power")
                if battery is not None:
                    return int(battery)
        return None

    @property
    def icon(self) -> str:
        """Return the icon based on battery level."""
        battery = self.native_value
        if battery is None:
            return "mdi:battery-unknown"
        if battery >= 90:
            return "mdi:battery"
        if battery >= 70:
            return "mdi:battery-70"
        if battery >= 50:
            return "mdi:battery-50"
        if battery >= 30:
            return "mdi:battery-30"
        if battery >= 10:
            return "mdi:battery-10"
        return "mdi:battery-outline"
