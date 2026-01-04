# Copyright (C) 2026 LoeLabs LLC - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# ~
"""Functions for interacting with the Supervisor API to find addon information."""
from __future__ import annotations

import os
import logging
from typing import Any, cast
from datetime import datetime, timedelta

from homeassistant.core import HomeAssistant  # pylint: disable=import-error
from homeassistant.helpers import aiohttp_client  # pylint: disable=import-error

from .const import (
    DOMAIN,
    ADDON_NAME_PUB,
    ADDON_NAME_DEV,
    ADDON_NAME_LOCAL,
    ADDON_PORT,
)

_LOGGER = logging.getLogger(__name__)

SUPERVISOR_URL = "http://supervisor"

# Cache for addon IP lookup
_cache: dict[str, tuple[str, datetime]] = {}


def _get_channel() -> str:
    """Get the current channel based on the DOMAIN."""
    if DOMAIN == "shf_bridge_local":
        return "local"
    # Default to "pub" for "shf_bridge" or any other domain
    return "pub"


def _get_addon_name_for_channel(channel: str) -> str:
    """Get the addon name for a given channel."""
    if channel == "dev":
        return ADDON_NAME_DEV
    if channel == "local":
        return ADDON_NAME_LOCAL
    return ADDON_NAME_PUB


async def _supervisor_get_json(hass: HomeAssistant, path: str) -> dict[str, Any]:
    """Call Supervisor API and return JSON response."""
    token = os.environ.get("SUPERVISOR_TOKEN")
    if not token:
        _LOGGER.error("SUPERVISOR_TOKEN not available (not running with Supervisor?)")
        raise RuntimeError("SUPERVISOR_TOKEN not available (not running with Supervisor?)")

    headers = {"Authorization": f"Bearer {token}"}
    url = f"{SUPERVISOR_URL}{path}"

    #_LOGGER.debug("Calling Supervisor API: %s", url)
    session = aiohttp_client.async_get_clientsession(hass)
    
    try:
        async with session.get(url, headers=headers, timeout=10) as resp:
            resp.raise_for_status()
            result = await resp.json()
            #_LOGGER.debug("Supervisor API response: %s", result)
            return cast(dict[str, Any], result)
    except Exception as e:  # pylint: disable=broad-exception-caught
        _LOGGER.error("Error calling Supervisor API %s: %s", url, e)
        raise


async def _find_addon_by_name(hass: HomeAssistant, addon_name: str) -> dict[str, Any] | None:
    """Find an addon by name from the Supervisor API."""
    data = await _supervisor_get_json(hass, "/addons")

    # Supervisor responses are usually {"data": {...}}; adjust if needed.
    addons = data.get("data", {}).get("addons", data.get("addons", []))

    for addon in addons:
        if isinstance(addon, dict) and addon.get("name") == addon_name:
            return cast(dict[str, Any], addon)

    return None


async def _get_addon_info(hass: HomeAssistant, addon_slug: str) -> dict[str, Any]:
    """Get the info for an addon from the Supervisor API."""
    data = await _supervisor_get_json(hass, f"/addons/{addon_slug}/info")

    # Supervisor responses are usually {"data": {...}}; adjust if needed.
    info = data.get("data", data)
    return cast(dict[str, Any], info)


async def get_addon_ip(hass: HomeAssistant) -> str:
    """
    Get the IP address of the addon for the current channel (determined from DOMAIN).
    
    Cached for 15 seconds to avoid excessive Supervisor API calls.
    
    Args:
        hass: Home Assistant instance
        
    Returns:
        IP address as a string (e.g., "172.30.33.6")
        
    Raises:
        RuntimeError: If addon not found or IP cannot be determined
    """
    channel = _get_channel()
    cache_key = f"addon_ip_{channel}"
    now = datetime.now()
    
    # Check cache
    if cache_key in _cache:
        cached_ip, cached_time = _cache[cache_key]
        if now - cached_time < timedelta(seconds=15):
            #_LOGGER.debug("Using cached addon IP for channel %s: %s", channel, cached_ip)
            return cached_ip
    
    # Cache miss or expired, fetch from Supervisor
    _LOGGER.debug("Fetching addon IP for channel %s from Supervisor", channel)
    
    addon_name = _get_addon_name_for_channel(channel)
    addon = await _find_addon_by_name(hass, addon_name)
    
    if not addon:
        raise RuntimeError(f"Addon '{addon_name}' not found")
    
    addon_slug = addon.get("slug")
    if not addon_slug:
        raise RuntimeError(f"Addon '{addon_name}' found but has no slug")
    
    # Get addon info to find IP
    info = await _get_addon_info(hass, addon_slug)


    ip_address = info.get('ip_address')
    if ip_address and isinstance(ip_address, str):
        _LOGGER.debug("Found addon IP from ip_address: %s", ip_address)
        _cache[cache_key] = (ip_address, now)
        return cast(str, ip_address)

    raise RuntimeError(f"Could not determine IP address for addon '{addon_name}' (slug: {addon_slug}).")
    


async def get_addon_base_url(hass: HomeAssistant) -> str:
    """
    Get the base URL for the addon (IP + port).
    
    Args:
        hass: Home Assistant instance
        
    Returns:
        Base URL as a string (e.g., "http://172.30.33.6:8099")
    """
    ip = await get_addon_ip(hass)
    return f"http://{ip}:{ADDON_PORT}"
