# Copyright (C) 2026 LoeLabs LLC - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# ~
"""The Smart Home Floorplan Bridge integration."""
from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.config_entries import ConfigEntry  # pylint: disable=import-error
from homeassistant.core import HomeAssistant  # pylint: disable=import-error

from .const import DOMAIN
from .proxy import ShfBridgeProxy, ShfBridgeStaticProxy

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Smart Home Floorplan Bridge from a config entry."""
    _LOGGER.info("Smart Home Floorplan Bridge: INITIALIZING")

    # Register API proxy view. Used for proxying api requests that can be called with hass.fetchWithAuth
    hass.http.register_view(ShfBridgeProxy)

    # Register static assets proxy view. Used for proxying static asset requests which come e.g. dirctly from html tags
    hass.http.register_view(ShfBridgeStaticProxy)

    # Initialize integration data structure
    hass.data.setdefault(DOMAIN, {})

    _LOGGER.info("Smart Home Floorplan Bridge: INITIALIZATION COMPLETE")
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    # Note: We don't unregister the static path or websocket handler
    # as they are shared resources. This is fine for this integration.
    return True
