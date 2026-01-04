"""The Smart Home Floorplan Bridge integration."""
from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.config_entries import ConfigEntry  # pylint: disable=import-error
from homeassistant.core import HomeAssistant  # pylint: disable=import-error
from homeassistant.components.http import StaticPathConfig  # pylint: disable=import-error

from .const import DOMAIN
from .websocket_api import async_register_ws
from .proxy import ShfBridgeProxy, ShfBridgeStaticProxy

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Smart Home Floorplan Bridge from a config entry."""
    _LOGGER.info("=" * 60)
    _LOGGER.info("Smart Home Floorplan Bridge: INITIALIZING")
    _LOGGER.info("Entry ID: %s", entry.entry_id)
    _LOGGER.info("Entry Title: %s", entry.title)
    _LOGGER.info("=" * 60)

    # Serve the card JS at /local/shf_bridge/shf-ha-frontend.js
    www_dir = Path(__file__).parent / "www"
    www_dir.mkdir(exist_ok=True)
    _LOGGER.info("Registering static path: /local/shf_bridge -> %s", www_dir)
    await hass.http.async_register_static_paths(
        [StaticPathConfig("/local/shf_bridge", str(www_dir), cache_headers=True)]
    )
    _LOGGER.info("✓ Static path registered successfully")

    # Register API proxy view
    _LOGGER.info("Registering API proxy view: /api/shf_bridge/proxy/*")
    hass.http.register_view(ShfBridgeProxy)
    _LOGGER.info("✓ API proxy view registered successfully")

    # Register static assets proxy view
    _LOGGER.info("Registering static proxy view: /local/shf_bridge/proxy/*")
    hass.http.register_view(ShfBridgeStaticProxy)
    _LOGGER.info("✓ Static proxy view registered successfully")

    # Register websocket API (commented out - using proxy instead)
    # _LOGGER.info("Registering websocket API handler: shf_bridge/get_ingress")
    # async_register_ws(hass)
    # _LOGGER.info("✓ Websocket API handler registered successfully")

    # Initialize integration data structure
    hass.data.setdefault(DOMAIN, {})
    _LOGGER.info("✓ Integration data structure initialized")

    _LOGGER.info("=" * 60)
    _LOGGER.info("Smart Home Floorplan Bridge: INITIALIZATION COMPLETE")
    _LOGGER.info("Integration is ready to use")
    _LOGGER.info("=" * 60)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Note: We don't unregister the static path or websocket handler
    # as they are shared resources. This is fine for this integration.
    return True
