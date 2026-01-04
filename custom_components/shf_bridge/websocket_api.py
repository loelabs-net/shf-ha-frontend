"""Websocket API for the Smart Home Floorplan Bridge integration."""
from __future__ import annotations

import logging
import os
from typing import Any, cast

import aiohttp  # pylint: disable=import-error

from homeassistant.core import HomeAssistant, callback  # pylint: disable=import-error

_LOGGER = logging.getLogger(__name__)

from .const import (
    ADDON_NAME_PUB,
    ADDON_NAME_DEV,
    ADDON_NAME_LOCAL,
)

SUPERVISOR_URL = "http://supervisor"


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

    _LOGGER.debug("Calling Supervisor API: %s", url)
    session = aiohttp.ClientSession()
    try:
        async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            resp.raise_for_status()
            result = await resp.json()
            _LOGGER.debug("Supervisor API response: %s", result)
            return cast(dict[str, Any], result)
    except aiohttp.ClientError as e:
        _LOGGER.error("Error calling Supervisor API %s: %s", url, e)
        raise
    finally:
        await session.close()


async def _find_addon_by_name(hass: HomeAssistant, addon_name: str) -> dict[str, Any] | None:
    """Find an addon by name from the Supervisor API."""
    data = await _supervisor_get_json(hass, "/addons")

    # Supervisor responses are usually {"data": {...}}; adjust if needed.
    addons = data.get("data", {}).get("addons", data.get("addons", []))

    for addon in addons:
        if isinstance(addon, dict) and addon.get("name") == addon_name:
            return cast(dict[str, Any], addon)

    return None


async def _get_ingress_url(hass: HomeAssistant, addon_slug: str) -> str:
    """Get the ingress URL for an addon. Returned with no trailing slash."""
    data = await _supervisor_get_json(hass, f"/addons/{addon_slug}/info")

    # Supervisor responses are usually {"data": {...}}; adjust if needed.
    info = data.get("data", data)

    # Common keys you'll see depending on Supervisor version:
    # - "ingress_url" (already a /hassio/ingress/<token>/ URL)
    # - OR pieces like "ingress_entry" that you turn into /hassio/ingress/<entry>/
    ingress_url = info.get("ingress_url")
    if ingress_url and isinstance(ingress_url, str):
        return ingress_url.rstrip("/")

    ingress_entry = info.get("ingress_entry")
    if ingress_entry and isinstance(ingress_entry, str):
        return f"/hassio/ingress/{ingress_entry}"

    raise RuntimeError(f"No ingress info found for add-on {addon_slug}")


# Websocket API handlers - COMMENTED OUT: Using proxy endpoint instead
# @callback
# def async_register_ws(hass: HomeAssistant) -> None:
#     """Register websocket API handlers."""

#     @websocket_api.websocket_command(
#         {
#             "type": "shf_bridge/get_ingress",
#             "channel": str,
#         }
#     )
#     @websocket_api.async_response
#     async def ws_get_ingress(hass: HomeAssistant, connection, msg):
#         """Handle websocket command to get addon ingress URL."""
#         channel = msg.get("channel", "pub")
#         addon_name = _get_addon_name_for_channel(channel)

#         _LOGGER.debug("Websocket request for channel: %s, addon_name: %s", channel, addon_name)

#         # Check cache first
#         cache = hass.data.setdefault(DOMAIN, {}).setdefault("cache", {})
#         cache_key = f"{channel}:{addon_name}"
#         now = time.time()
#         cached = cache.get(cache_key)
#         if cached and (now - cached["ts"] < DEFAULT_CACHE_SECONDS):
#             _LOGGER.debug("Returning cached result for %s", cache_key)
#             connection.send_result(
#                 msg["id"],
#                 {
#                     "ingress_url": cached["ingress_url"],
#                     "addon_slug": cached["addon_slug"],
#                 },
#             )
#             return

#         try:
#             # Find addon by name
#             _LOGGER.debug("Searching for addon: %s", addon_name)
#             addon = await _find_addon_by_name(hass, addon_name)
#             if not addon:
#                 _LOGGER.warning("Add-on '%s' not found", addon_name)
#                 connection.send_error(
#                     msg["id"],
#                     "addon_not_found",
#                     f"Add-on '{addon_name}' not found. Please ensure the Smart Home Floorplan add-on is installed.",
#                 )
#                 return

#             addon_slug = addon.get("slug")
#             if not addon_slug:
#                 _LOGGER.error("Add-on '%s' found but slug is missing", addon_name)
#                 connection.send_error(
#                     msg["id"],
#                     "addon_error",
#                     f"Add-on '{addon_name}' found but slug is missing.",
#                 )
#                 return

#             # Get ingress URL
#             _LOGGER.debug("Getting ingress URL for addon slug: %s", addon_slug)
#             ingress_url = await _get_ingress_url(hass, addon_slug)

#             # Cache the result
#             cache[cache_key] = {
#                 "ts": now,
#                 "ingress_url": ingress_url,
#                 "addon_slug": addon_slug,
#             }

#             _LOGGER.info("Successfully resolved ingress for %s: %s", addon_name, ingress_url)
#             connection.send_result(
#                 msg["id"],
#                 {
#                     "ingress_url": ingress_url,
#                     "addon_slug": addon_slug,
#                 },
#             )
#         except (RuntimeError, aiohttp.ClientError) as e:
#             _LOGGER.exception("Error getting ingress URL for %s: %s", addon_name, e)
#             connection.send_error(
#                 msg["id"],
#                 "ingress_error",
#                 f"Error getting ingress URL: {str(e)}",
#             )

#     async_register_command(hass, ws_get_ingress)


@callback  # type: ignore[misc]
def async_register_ws(hass: HomeAssistant) -> None:
    """Register websocket API handlers (currently disabled - using proxy instead)."""
