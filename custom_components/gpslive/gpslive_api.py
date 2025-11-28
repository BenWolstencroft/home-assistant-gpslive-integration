"""API client for GPSLive."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp

from .const import API_BASE_URL, API_TIMEOUT

_LOGGER = logging.getLogger(__name__)


class GPSLiveAPI:
    """GPSLive API client."""

    def __init__(self, api_key: str, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self.api_key = api_key
        self.session = session
        self.base_url = API_BASE_URL

    async def _request(
        self, method: str, endpoint: str, **kwargs: Any
    ) -> dict[str, Any] | list[Any]:
        """Make a request to the API."""
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        
        try:
            async with asyncio.timeout(API_TIMEOUT):
                async with self.session.request(
                    method, url, headers=headers, **kwargs
                ) as response:
                    if response.status == 401:
                        raise GPSLiveAuthError("Invalid API key")
                    if response.status == 403:
                        raise GPSLiveAuthError("Access forbidden")
                    
                    response.raise_for_status()
                    return await response.json()
        except asyncio.TimeoutError as err:
            raise GPSLiveConnectionError("Request timeout") from err
        except aiohttp.ClientError as err:
            raise GPSLiveConnectionError(f"Connection error: {err}") from err

    async def get_devices(self) -> list[dict[str, Any]]:
        """Get all devices with last known locations."""
        response = await self._request("GET", "/v1/devices/list")
        return response if isinstance(response, list) else []

    async def get_devices_detailed(self) -> list[dict[str, Any]]:
        """Get detailed device information including sensors and drivers."""
        response = await self._request("GET", "/v1/devices")
        return response if isinstance(response, list) else []

    async def get_device_locations(self, imeis: list[str]) -> list[dict[str, Any]]:
        """Get last known locations for specific devices."""
        response = await self._request(
            "POST", "/v1/devices/locations", json={"imeis": imeis}
        )
        return response if isinstance(response, list) else []


class GPSLiveError(Exception):
    """Base exception for GPSLive errors."""


class GPSLiveAuthError(GPSLiveError):
    """Exception for authentication errors."""


class GPSLiveConnectionError(GPSLiveError):
    """Exception for connection errors."""
