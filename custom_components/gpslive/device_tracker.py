"""Support for GPSLive device trackers."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.device_tracker import SourceType, TrackerEntity
from homeassistant.config_entries import ConfigEntry
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
    """Set up GPSLive device tracker based on a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]
    
    entities = []
    for device in coordinator.data:
        entities.append(GPSLiveDeviceTracker(coordinator, device))
    
    async_add_entities(entities)


class GPSLiveDeviceTracker(CoordinatorEntity, TrackerEntity):
    """Representation of a GPSLive device tracker."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        device: dict[str, Any],
    ) -> None:
        """Initialize the device tracker."""
        super().__init__(coordinator)
        self._device = device
        self._attr_unique_id = f"gpslive_{device.get('imei')}"
        self._attr_name = device.get("name", f"GPSLive {device.get('plateNumber', device.get('imei'))}")

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information about this entity."""
        return {
            "identifiers": {(DOMAIN, self._device.get("imei"))},
            "name": self._attr_name,
            "manufacturer": "GPSLive",
            "model": self._device.get("protocol", "GPS Tracker"),
        }

    @property
    def source_type(self) -> SourceType:
        """Return the source type of the device."""
        return SourceType.GPS

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        return self._device.get("lat")

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        return self._device.get("lng")

    @property
    def battery_level(self) -> int | None:
        """Return the battery level of the device."""
        if params := self._device.get("params"):
            if isinstance(params, dict):
                # Battery level might be in params.battery or params.power
                return params.get("battery") or params.get("power")
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra attributes."""
        attrs = {}
        
        # Add attributes from the device data
        if imei := self._device.get("imei"):
            attrs["imei"] = imei
        if plate := self._device.get("plateNumber"):
            attrs["plate_number"] = plate
        if speed := self._device.get("speed"):
            attrs["speed"] = speed
        if odometer := self._device.get("odometer"):
            attrs["odometer"] = odometer
        if dt_tracker := self._device.get("dtTracker"):
            attrs["last_update"] = dt_tracker
        if protocol := self._device.get("protocol"):
            attrs["protocol"] = protocol
        if active := self._device.get("active"):
            attrs["active"] = active
        
        # Add params if available
        if params := self._device.get("params"):
            if isinstance(params, dict):
                attrs["params"] = params
        
        return attrs

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Find updated device data by IMEI
        for device in self.coordinator.data:
            if device.get("imei") == self._device.get("imei"):
                self._device = device
                break
        
        super()._handle_coordinator_update()
