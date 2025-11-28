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
        self._attr_unique_id = f"gpslive_{device.get('id', device.get('device_id'))}"
        self._attr_name = device.get("name", f"GPSLive Device {device.get('id')}")

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information about this entity."""
        return {
            "identifiers": {(DOMAIN, self._device.get("id", self._device.get("device_id")))},
            "name": self._attr_name,
            "manufacturer": "GPSLive",
            "model": self._device.get("model", "GPS Tracker"),
        }

    @property
    def source_type(self) -> SourceType:
        """Return the source type of the device."""
        return SourceType.GPS

    @property
    def latitude(self) -> float | None:
        """Return latitude value of the device."""
        # Update these based on your API response structure
        if location := self._device.get("location"):
            return location.get("latitude") or location.get("lat")
        return self._device.get("latitude") or self._device.get("lat")

    @property
    def longitude(self) -> float | None:
        """Return longitude value of the device."""
        # Update these based on your API response structure
        if location := self._device.get("location"):
            return location.get("longitude") or location.get("lng") or location.get("lon")
        return self._device.get("longitude") or self._device.get("lng") or self._device.get("lon")

    @property
    def battery_level(self) -> int | None:
        """Return the battery level of the device."""
        return self._device.get("battery_level") or self._device.get("battery")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra attributes."""
        attrs = {}
        
        # Add any additional attributes from the device data
        for key in ["speed", "heading", "altitude", "accuracy", "timestamp", "last_update"]:
            if value := self._device.get(key):
                attrs[key] = value
        
        return attrs

    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        # Find updated device data
        for device in self.coordinator.data:
            device_id = device.get("id", device.get("device_id"))
            if device_id == self._device.get("id", self._device.get("device_id")):
                self._device = device
                break
        
        super()._handle_coordinator_update()
